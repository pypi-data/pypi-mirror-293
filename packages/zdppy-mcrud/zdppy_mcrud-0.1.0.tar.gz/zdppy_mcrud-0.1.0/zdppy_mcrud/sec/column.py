import re


def is_sec_add_table_column(s):
    """判断是否为安全的新增表格的column"""
    if type(s) is not str:
        return False

    # 不能有敏感内容
    if ";" in s:
        return False
    if "drop" in s:
        return False
    if "select" in s:
        return False
    if "truncate" in s:
        return False
    if "delete" in s:
        return False

    # 清洗
    s = s.replace("\\", "")
    s = s.replace(" ", "")
    s = s.replace("[", "")
    s = s.replace("]", "")
    s = s.replace("{", "")
    s = s.replace("}", "")
    s = s.replace("：", "")
    s = s.replace(":", "")
    s = s.replace(">", "")
    s = s.replace("<", "")
    s = s.replace("=", "")
    s = s.replace(".", "")
    s = s.replace("'", "")
    s = s.replace("\"", "")

    # 正则
    if re.match(r"^[a-zA-Z0-9_()\u4e00-\u9fa5]+$", s) is None:
        return False

    slen = len(s)
    return 128 > slen > 3


def is_sec_column(s):
    """判断是否为安全的列名"""
    if not isinstance(s, str):
        return False
    if s == "*":
        return True
    return re.match(r"^\w+$", str(s)) is not None


def is_sec_columns(s):
    """判断是否为安全的列名列表"""
    if not isinstance(s, str):
        return False

    # 替换空格 a , b , c  => a,b,c
    s = s.replace(" ", "")
    columns = s.split(",")

    # 所有列都得安全
    return all(map(is_sec_column, columns))
