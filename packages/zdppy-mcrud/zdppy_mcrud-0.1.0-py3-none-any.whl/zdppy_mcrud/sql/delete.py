from ..db.exceptions import ErrorArgException


def delete_by_condition(table, condition_dict):
    """
    获取添加数据的字符串
    :param table:
    :return:
    """
    # 校验数据类型
    if not isinstance(condition_dict, dict):
        raise ErrorArgException("查询条件 condition_dict 应该是字典类型")
    if not isinstance(table, str):
        raise ErrorArgException("table 参数应该是字符串类型")

    # 要删除的条件
    conditions = []
    for k, v in condition_dict.items():
        if v is None:
            conditions.append(f"{k} is null")
        else:
            conditions.append(f"{k}='{v}'")
    condition_str = " and ".join(conditions)

    # 准备sql
    s = f"delete from {table} where {condition_str};"
    return s
