from .. import sql
from .base import IBase
from .. import sec
from zdppy_log import logger


class __Delete(IBase):
    """
    注意：这个类会被用于继承了DatabaseBase的类中
    """

    def delete_database(self, database):
        """删除数据库"""
        sql = f"drop database if exists {database};"
        logger.debug("准备删除数据库", database=database, sql=sql)
        self.execute(sql)
        logger.debug("删除数据库成功", database=database, sql=sql)

    def delete_table(self, table):
        """删除表"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        sql = f"drop table if exists {table};"
        self.execute(sql)

    def delete_index(self, table, column):
        """删除索引"""
        # 校验table
        if not sec.is_sec_table(table):
            return
        # 校验列
        if not sec.is_sec_column(column):
            return
        # SQL语句
        s = f"drop index idx_{column} on {table};"
        self.execute(s)

    def delete(self, table, _id):
        """根据id删除数据"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        s = sql.get_sql_delete_by_id(table)
        self.execute(s, [_id])

    def delete_by_ids(self, table, ids):
        """根据id列表删除数据"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        # 传的不是字符串
        if type(table) is not str or len(table) == 0:
            return

        # 传的不是列表
        if type(ids) is not list:
            return
        # 获取SQL语句
        s = sql.get_sql_delete_by_ids(table, len(ids))
        self.execute(s, ids)

    def delete_all(self, table):
        """清空表中的数据"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        s = f"truncate table {table}"
        self.execute(s)

    def delete_by(self, table, condition_dict):
        """
        根据条件删除数据
        :param table 表格名称
        :param condition_dict 条件字典，比如 {id:1} 表示修改id为1的数据
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        s = sql.delete_by_condition(table, condition_dict)
        self.execute(s)
