import re


def is_sec_order(s):
    """判断是否为安全的排序名"""
    if not isinstance(s, str):
        return False
    return re.match(r"^\w+$", str(s)) is not None


def is_sec_orders(s):
    """判断是否为安全的排序名"""
    if not isinstance(s, str):
        return False

    # 替换空格 id desc, name asc  => iddesc,nameasc
    s = s.replace(" ", "")
    orders = s.split(",")

    # 所有列都得安全
    return all(map(is_sec_order, orders))
