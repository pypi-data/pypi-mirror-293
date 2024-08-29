from .. import sql
from .. import sec
from .base import IBase
from zdppy_log import logger


class __Add(IBase):
    """
    注意：这个类会被用于继承了DatabaseBase的类中
    """

    def add_database(self, database, charset="utf8mb4"):
        """添加数据库"""
        s = f"create database if not exists {database} character set {charset};"
        self.execute(s)

    def add_database_force(self, database):
        """强制添加数据库，如果已存在，则先删除"""
        self.delete_database(database)
        self.add_database(database)

    def add(self, table, columns, values):
        """添加数据"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        columns = [str(v) for v in columns]
        s = sql.get_add_sql(table, columns)
        self.execute(s, values)

    def add_by_dict(
            self,
            table: str,
            columns_values_dict: dict
    ):
        """添加数据"""
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        columns = list(columns_values_dict.keys())
        columns = [str(v) for v in columns]
        s = sql.get_add_sql(table, columns)
        self.execute(s, list(columns_values_dict.values()))

    def add_column(
            self,
            table,
            column,
            column_type="varchar(255)",
            default_value="null",
            comment="",
    ):
        """添加一列"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        s = sql.get_add_column_sql(table, column, column_type, default_value, comment)
        logger.debug(
            "为表添加新的一列",
            table=table,
            column=column,
            column_type=column_type,
            sql=s,

        )
        self.execute(s)

    def add_many(self, table, columns, values):
        """批量插入"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 获取SQL语句
        columns = [str(v) for v in columns]
        s = sql.get_add_sql(table, columns)
        # 执行新增
        self.execute_many(s, values)

    def add_by_sql_file(self, file_path) -> None:
        """根据SQL文件导入数据, SQL 文件一行是一个 insert 语句"""
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.execute(line.strip())

    def add_config_value(self, table, config_name, config_value):
        """
        设置配置值
        要求表格包含两个列名：name 和 value
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        sql = f"insert into `{table}` (name, value) values (%s, %s);"
        try:
            self.execute(sql, [config_name, config_value])
        except Exception as e:
            if "Duplicate entry" not in str(e):
                raise e

    def add_index(self, table, column):
        """添加索引"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 校验列
        if not sec.is_sec_column(column):
            return
        # SQL语句
        s = f"create index idx_{column} on {table} (`{column}`);"
        self.execute(s)

    def add_table(
            self,
            table,
            columns=None,
            engine="innodb",
            charset="utf8mb4",
            is_str_id=True,
            is_add_time=True,
            is_update_time=True,
            is_delete=True,
    ):
        """添加表格"""
        # 参数校验
        if not isinstance(columns, list) or len(columns) == 0:
            logger.error("columns应该是字符串列表，请检查后重试", columns=columns)
            return

        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        if not all(map(sec.is_sec_add_table_column, columns)):
            logger.error("不安全的列名，请检查后重试", table=table, columns=columns)
            return

        # ID列
        idstr = "id int primary key auto_increment"
        if is_str_id:
            idstr = "id varchar(36) primary key"
        columns.append(idstr)
        # 新增时间列
        if is_add_time:
            add_time_str = "add_time datetime default current_timestamp"
            columns.append(add_time_str)
        # 更新时间列
        if is_update_time:
            update_time_str = "update_time datetime default current_timestamp on update current_timestamp"
            columns.append(update_time_str)
        # 是否删除
        if is_delete:
            is_delete_str = "is_delete bool default 0"
            columns.append(is_delete_str)

        # 建表SQL
        column_str = ",".join(columns)
        _sql = f"""create table if not exists {table}(
            {column_str}
        )engine={engine} character set {charset}"""
        logger.debug("生成建表SQL语句成功", sql=_sql)

        # 执行
        return self.execute(_sql)
