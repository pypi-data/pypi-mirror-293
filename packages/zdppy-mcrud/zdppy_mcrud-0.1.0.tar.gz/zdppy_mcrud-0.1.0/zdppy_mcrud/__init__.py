from zdppy_mcrud.db.database import Database
from .db.db import new
from .db.env import new_env

__all__ = [
    "Database",  # 数据库核心对象
    "new",  # 根据环境变量获取DB
    "new_env",  # 根据环境变量获取DB
]
