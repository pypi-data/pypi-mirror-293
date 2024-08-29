import os
from .database import Database


def new_env(ssl=None):
    """根据环境变量获取Database对象"""
    # 读取环境变量
    MCRUD_HOST = os.getenv("ZDPPY_MCRUD_HOST")
    MCRUD_PORT = os.getenv("ZDPPY_MCRUD_PORT")
    MCRUD_DATABASE = os.getenv("ZDPPY_MCRUD_DATABASE")
    MCRUD_USERNAME = os.getenv("ZDPPY_MCRUD_USERNAME")
    MCRUD_PASSWORD = os.getenv("ZDPPY_MCRUD_PASSWORD")
    try:
        MCRUD_PORT = int(MCRUD_PORT)
    except:
        return

    # 获取数据库对象
    db = None
    if MCRUD_HOST and MCRUD_PORT and MCRUD_USERNAME and MCRUD_PASSWORD:
        # 获取数据库对象
        db = Database(
            host=MCRUD_HOST,
            port=MCRUD_PORT,
            username=MCRUD_USERNAME,
            password=MCRUD_PASSWORD,
        )
        if MCRUD_DATABASE is None or MCRUD_DATABASE == "":
            return db

        # 判断数据库是否存在
        if db.has_database(MCRUD_DATABASE):
            db = Database(
                host=MCRUD_HOST,
                port=MCRUD_PORT,
                username=MCRUD_USERNAME,
                password=MCRUD_PASSWORD,
                database=MCRUD_DATABASE,
            )
            return db

        # 如果不存在，则新建数据库
        db.add_database(MCRUD_DATABASE)
        db = Database(
            host=MCRUD_HOST,
            port=MCRUD_PORT,
            username=MCRUD_USERNAME,
            password=MCRUD_PASSWORD,
            database=MCRUD_DATABASE,
        )
        return db
