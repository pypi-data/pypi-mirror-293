from zdppy_mcrud import sec
from .base import DatabaseBase
from .add import __Add
from .delete import __Delete
from .update import __Update
from .get import __Get
from .has import __Has


class Database(DatabaseBase, __Add, __Delete, __Update, __Get, __Has):
    """数据库操作类"""

    def __init__(self, host="localhost", port=3306, username="root", password="root", database="", charset="utf8mb4"):
        """
        创建数据库连接对象的初始化方法
        @param host 数据库主机地址
        @param port 数据库端口号
        @param username 用户名
        @param password 密码
        @param database 数据库
        @param charset 字符集
        """
        super().__init__(host, port, username, password, database, charset)

    def export_csv(
            self,
            table,
            columns,
            csv_file_name,
            limit=100,
    ):
        """
        导出表格数据为 CSV 文件
        """

        def get_sql(limit, offset):
            """获取查询 SQL 语句"""
            sql = "select "
            for i in range(len(columns) - 1):
                sql += f"`{columns[i]}`, "
            else:
                sql += f"`{columns[-1]}` "
            sql += f"from {table} limit {limit} offset {offset};"
            return sql

        def get_csv_line(data):
            """获取 CSV 的一行数据"""
            line = ""
            for i in range(len(columns) - 1):
                line += f"{data.get(columns[i])},"
            else:
                line += f"{data.get(columns[-1])}\n"
            return line

        with open(csv_file_name, "w+", encoding="utf-8") as f:
            """查询数据库数据并写入 CSV 文件"""
            self.re_connection()
            with self.connection.cursor() as cursor:
                offset = 0
                while True:
                    sql = get_sql(limit, offset)
                    cursor.execute(sql)
                    data_list = cursor.fetchall()
                    for data in data_list:
                        f.write(get_csv_line(data))
                    offset += limit
                    if len(data_list) < limit:
                        break
