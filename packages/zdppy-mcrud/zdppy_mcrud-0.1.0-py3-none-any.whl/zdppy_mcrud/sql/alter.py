from .. import sec


def get_add_column_sql(
        table,
        column,
        column_type="varchar(255)",
        default_value="null",
        comment=None,
):
    """
    获取新增一列的SQL
    :param table: 要修改的表格名
    :param column: 要增加的列名
    :param column_type: 要增加的列的类型
    :param default_value: 默认值
    :param comment: 列的提示内容
    """
    # 校验数据类型
    if type(table) is not str:
        return
    if type(column) is not str:
        return
    if type(column_type) is not str:
        return

    # 校验非法字符
    if not sec.is_sec_str(table):
        return
    if not sec.is_sec_str(column):
        return
    if not sec.is_sec_colum_type(column_type):
        return
    if not sec.is_sec_default_value(default_value):
        return

    # 处理特殊类型
    column_type = column_type.lower()
    if column_type == "bool":
        default_value = 1 if default_value else 0

    # SQL语句
    sql = f"alter table `{table}` add column `{column}` {column_type} default '{default_value}'"
    if comment is not None and sec.is_sec_comment(comment):
        sql = f"{sql} comment '{comment}'"
    return sql
