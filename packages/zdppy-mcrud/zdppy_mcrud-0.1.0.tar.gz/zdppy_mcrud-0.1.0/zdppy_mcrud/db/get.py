import datetime
from .. import sql
from .base import IBase
from .. import sec
from .exceptions import ErrorArgException
from zdppy_log import logger


class __Get(IBase):
    """
    注意：这个类会被用于继承了DatabaseBase的类中
    """

    def get_all_database(self, is_contains_inner=False):
        """查看所有数据库"""
        results = self.fetchall("show databases")
        databases = {item.get("Database") for item in results}
        # 移除内置的数据库
        inner_databases = {
            "information_schema",
            "mysql",
            "performance_schema",
            "sys",
        }
        if is_contains_inner:
            results = databases
        else:
            results = databases - inner_databases
        logger.debug(
            "获取所有数据库成功",
            databases=databases,
            inner_databases=inner_databases,
            results=results,
        )
        return list(results)

    def get_table_sql(self, table):
        """获取创建表格的 SQL 语句"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        results = self.fetchall(f"show create table {table}")
        if len(results) > 0:
            result = results[0]
            return result.get("Create Table")

    def get_table_columns(self, table):
        """获取表格的所有字段"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 获取建表语句
        table_sql = self.get_table_sql(table)

        # 切割关键字
        columns_list = table_sql.split(" ")

        # 提取列名
        columns = []
        for column in columns_list:
            if column.startswith("`") and column.endswith("`"):
                columns.append(column.replace("`", ""))

        # 返回，第一个是表名，所以要去掉
        new_columns = []
        for column in columns[1:]:
            if column not in new_columns:
                new_columns.append(column)
        return new_columns

    def get_all_table(self):
        """查看所有表格"""
        results = self.fetchall("show tables")
        return [item.get(f"Tables_in_{self.database}") for item in results]

    def get_the_column(
            self,
            table,
            column,
    ):
        """
        查询指定字段的所有值
        @param connection: 连接对象
        @param column: 字段名
        @param size: 每次查询数量
        @param offset: 每次查询偏移量
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        total = self.get_total(table)
        if total > 100000:
            print("数据量超过10w，直接查询耗时可能较长，推荐使用 get_the_column_generator 获取生成器")

        name_list = []
        offset = 0
        size = 100
        while True:
            sql = f"SELECT {column} from {table} order by id limit %s offset %s"
            results = self.fetchall(sql, [size, offset])
            name_list.extend([v.get(column) for v in results])
            offset += size
            if len(results) < size:
                break
        return name_list

    def get_the_column_generator(
            self,
            table,
            column,
    ):
        """
        查询指定字段的所有值
        @param connection: 连接对象
        @param column: 字段名
        @param size: 每次查询数量
        @param offset: 每次查询偏移量
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        offset = 0
        size = 100
        while True:
            sql = f"SELECT {column} from {table} order by id limit %s offset %s"
            results = self.fetchall(sql, [size, offset])
            for v in results:
                yield v.get(column)
            offset += size
            if len(results) < size:
                break

    def get_all(
            self,
            table,
            columns=None,
            offset=0,
            limit=20,
            order_str="id desc",
            parse_date_time=False,
            query=None,
    ):
        """
        查询表格中的所有数据
        :param table 表格名
        :param columns 必须是字符串列表类型
        :param order_str 排序内容
        :param offset 偏移值
        :param limit 每页查询的数量
        :param parse_date_time 是否需要解析时间类型的字段
        :param query 查询字典
        """
        # 处理要查询的列
        if columns is None:
            columns = "*"
        else:
            if not isinstance(columns, list):
                raise ErrorArgException(f"columns必须是数组类型：{columns}")
            try:
                columns = ",".join(columns)
            except Exception as e:
                logger.error("处理columns失败", columns=columns, err=e)
                raise ErrorArgException("columns格式错误，请确保元素都是字符串类型")
        if not isinstance(offset, int) or offset < 0:
            logger.error("offset必须为大于或等于0的整数", offset=offset)
            return
        if not isinstance(limit, int) or limit < 0:
            logger.error("limit必须为大于或等于0的整数", offset=offset)
            return

        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        if not sec.is_sec_columns(columns):
            logger.error("不安全的列名，请检查后重试", table=table, columns=columns)
            return
        if not sec.is_sec_orders(order_str):
            logger.error("不安全的排序字段，请检查后重试", table=table, columns=columns, order_str=order_str)
            return

        # 拼接SQL
        _sql = f"select {columns} from {table}"

        # condition
        if isinstance(query, dict):
            conditions = []
            for k, v in query.items():
                if k in columns:
                    if v == "notnull":
                        conditions.append(f"{str(k)} is not null")
                    else:
                        conditions.append(f"{str(k)}='{str(v)}'")
            condition = " and ".join(conditions)
            if condition:
                _sql = f"{_sql} where {condition}"

        # 排序
        if order_str is not None:
            _sql = f"{_sql} order by {order_str}"
        # 分页
        _sql = f"{_sql} limit {limit} offset {offset}"
        logger.debug("执行get_all查询", table=table, columns=columns, sql=_sql)

        # 执行查询
        data = self.fetchall(_sql)

        # 解析时间类型
        if parse_date_time:
            data = self.__parse_datetime(data)

        # 返回
        return data

    def __parse_datetime(self, data):
        if isinstance(data, list):
            new_data = []
            for v in data:
                if not isinstance(v, dict):
                    return data
                new_data.append(self.__parse_datetime_dict(v))
            return new_data
        elif isinstance(data, dict):
            return self.__parse_datetime_dict(data)

    def __parse_datetime_dict(self, data_dict):
        if not isinstance(data_dict, dict):
            return {}

        item = {}
        for k, vv in data_dict.items():
            if isinstance(vv, datetime.datetime):
                vv = vv.strftime("%Y-%m-%d %H:%M:%S")
            item[k] = vv
        return item

    def get_all_distinct(self, table, column):
        """去重查询表格中的某列数据"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        if not sec.is_sec_column(column):
            logger.error("不安全的列名，请检查后重试", table=table, column=column)
            return

        # 执行SQL
        _sql = f"select distinct {column} from {table}"
        results = self.fetchall(_sql)
        if len(results) > 0:
            return [result.get(column) for result in results]

    def get_config_value(self, table, config_name):
        """
        获取表格中指定字段的值
        要求表格包含两个列名：name 和 value
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        if not sec.is_sec_column(config_name):
            logger.error("不安全的列名，请检查后重试", table=table, column=config_name)
            return

        # 执行查询
        _sql = f"select value from `{table}` where name=%s"
        results = self.fetchall(_sql, args=[config_name])
        if len(results) > 0:
            return results[0].get("value")

    def get_by_id(self, table, tid, parse_datetime=True):
        """
        根据 ID 查询表格的特定行
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        if not sec.is_sec_id(tid):
            logger.error("不安全的ID，请检查后重试", table=table, column=tid)
            return

        # 执行查询
        _sql = f"select * from {table} where id = %s;"
        result = self.fetchone(_sql, [tid])

        # 解析时间
        if parse_datetime:
            result = self.__parse_datetime_dict(result)

        return result

    def get_by_ids(self, table, ids, parse_datetime=False):
        """
        根据 ID 列表查询表格的特定行
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        if not sec.is_sec_ids(ids):
            logger.error("不安全的ID，请检查后重试", table=table, ids=ids)
            return

        # 执行查询
        tid = ",".join([f"'{_id}'" for _id in ids])
        _sql = f"select * from {table} where id in ({tid});"
        data = self.fetchall(_sql)

        # 解析时间
        if parse_datetime:
            data = self.__parse_datetime(data)

        # 返回
        return data

    def get_total(self, table):
        """
        获取表格中的数据总数
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 执行查询
        _sql = f"select count(*) as count from {table}"
        result = self.fetchone(_sql)
        return result.get("count")

    def get_count_id(self, table):
        """
        获取表格中的ID的个数
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 执行查询
        _sql = f"select count(id) as count from {table}"
        result = self.fetchone(_sql)
        return result.get("count")

    def get(self, _sql, parse_datetime=True, *args):
        """查询单条数据"""
        data = self.fetchone(_sql, args)
        if parse_datetime:
            data = self.__parse_datetime_dict(data)
        return data

    def get_by(self, table, condition_dict, parse_datetime=True):
        """根据条件查询数据"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 执行查询
        _sql = sql.get_by_condition(table, condition_dict)
        data = self.fetchall(_sql)

        # 解析时间
        if parse_datetime:
            data = self.__parse_datetime(data)

        # 返回
        return data

    def get_index(self, table):
        """查看索引"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 执行查询
        r = self.fetchall(f"show index from {table}")

        # 封装并返回
        return [
            {
                "index": v.get("Key_name"),
                "column": v.get("Column_name")
            }
            for v in r
        ]

    def get_ids(self, table):
        """
        get all id of the table
        """
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        r = self.fetchall(f"select id from {table}")
        ids = [item.get('id') for item in r]
        return ids
