from .base import IBase
from .. import sec

has_logger = False
try:
    from log import logger

    has_logger = True
except:
    pass


class __Has(IBase):
    """
    注意：这个类会被用于继承了DatabaseBase的类中
    """

    def has_table(self, table):
        """判断表格是否都存在"""
        # 安全性校验
        if not sec.is_sec_table(table):
            if has_logger:
                logger.error("不安全的表名，请检查后重试", table=table)
            return

        tables = self.get_all_table()
        if not isinstance(tables, list):
            return False
        return table in tables

    def has_database(self, database):
        """判断数据库是否都存在"""
        databases = self.get_all_database()
        if not isinstance(databases, list):
            return False
        return database in databases
