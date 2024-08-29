from ..db.exceptions import ErrorArgException


def update_by_condition(table, condition_dict, columns):
    """
    获取添加数据的字符串
    :param table:
    :param columns:
    :return:
    """
    # 校验数据类型
    if not isinstance(condition_dict, dict):
        raise ErrorArgException("查询条件 condition_dict 应该是字典类型")
    if not isinstance(table, str):
        raise ErrorArgException("table 参数应该是字符串类型")
    if not isinstance(columns, list):
        raise ErrorArgException("columns 参数应该是列表类型")

    # 要修改的值
    kvs = [f"{columns[i]}=%s" for i in range(len(columns))]
    kvstr = ", ".join(kvs)

    # 要修改的条件
    conditions = []
    for k, v in condition_dict.items():
        if v is None:
            conditions.append(f"{k} is null")
        else:
            conditions.append(f"{k}='{v}'")
    condition_str = " and ".join(conditions)

    # 准备sql
    s = f"update {table} set {kvstr} where {condition_str};"
    return s
