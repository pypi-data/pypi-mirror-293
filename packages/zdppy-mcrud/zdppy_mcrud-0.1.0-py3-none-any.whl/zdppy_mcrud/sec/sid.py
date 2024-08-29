import re


def is_sec_id(s):
    """判断是否为安全的ID"""
    # 替换字符串
    sid = str(s)
    sid = sid.replace("-", "")
    sid = sid.replace("$", "")
    # 校验长度
    id_len = len(sid)
    if id_len < 1 or id_len > 36:
        return False
    # 校验内容
    return re.match(r"^\w+$", sid) is not None


def is_sec_ids(ids):
    """是否为安全的ID列表"""
    return all(map(is_sec_id, ids))
