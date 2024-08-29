import re


def is_sec_str(s):
    """判断是否为安全的字符串"""
    return re.match(r"^\w+$", str(s)) is not None


def is_sec_table(s):
    """判断是否为安全的表名"""
    if not s:
        return False
    return re.match(r"^\w+$", str(s)) is not None


def is_sec_column(s):
    """判断是否为安全的列名"""
    return is_sec_table(s)


def is_sec_default_value(s):
    """判断是否为安全的默认值"""
    return re.match(r"^[\s\w\.:/-]+$", str(s)) is not None


def is_sec_colum_type(s):
    """判断是否为安全的列类型"""
    if type(s) is not str:
        return False
    return re.match(r"^[a-zA-Z0-9_()]+$", s) is not None


def is_sec_comment(s):
    """判断是否为安全的列注释"""
    if type(s) is not str:
        return False
    if re.match(r"^[a-zA-Z0-9_()、:：\s\[\]{}><=\.\u4e00-\u9fa5]+$", s) is None:
        return False
    return len(s) < 128


if __name__ == '__main__':
    print(is_sec_comment("1、成功 2：:失败"))
