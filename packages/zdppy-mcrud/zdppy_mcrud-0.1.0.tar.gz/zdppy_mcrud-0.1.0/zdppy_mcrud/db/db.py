import os.path
from .database import Database


def new(
        host="127.0.0.1",
        port=3306,
        username="root",
        password="zhangdapeng520",
        database=""
):
    return Database(
        host=host,
        port=port,
        database=database,
        username=username,
        password=password,
    )
