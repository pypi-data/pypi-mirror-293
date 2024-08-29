import datetime

from .. import sql
from .base import IBase
from .. import sec
from zdppy_log import logger


class __Update(IBase):
    """
    注意：这个类会被用于继承了DatabaseBase的类中
    """

    def update(self, table, _id, columns, values):
        """根据id修改数据"""
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return
        columns = [str(v) for v in columns]
        s = sql.get_sql_update_by_id(table, columns)
        values.append(_id)
        self.execute(s, values)

    def update_datetime(self, table, _id, column, value=datetime.datetime.now()):
        """根据id修改时间类型数据"""
        return self.update(
            table,
            _id,
            [column],
            [value],
        )

    def update_datetime_now(self, table, _id, column):
        """根据id修改时间类型数据为当前时间"""
        return self.update(
            table,
            _id,
            [column],
            [datetime.datetime.now()],
        )

    def update_by(self, table, condition_dict, columns, values):
        """
        根据条件修改数据
        :param condition_dict 条件字典，比如 {id:1} 表示修改id为1的数据
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        columns = [str(v) for v in columns]
        s = sql.update_by_condition(table, condition_dict, columns)
        self.execute(s, values)

    def update_config_value(self, table, config_name, config_value):
        """
        修改配置值
        要求表格包含两个列名：name 和 value
        """
        # 安全性校验
        if not sec.is_sec_table(table):
            logger.error("不安全的表名，请检查后重试", table=table)
            return

        sql = f"update `{table}` set value=%s where name=%s;"
        self.execute(sql, [config_value, config_name])
