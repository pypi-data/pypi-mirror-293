import time
from zdppy_mysql.cursors import DictCursor
from zdppy_mysql.connections import Connection
from .exceptions import NoImplementException
from zdppy_log import logger


class IBase:
    """基础接口"""

    def execute(self, sql_str, args=None):
        """执行SQL语句"""
        raise NoImplementException()

    def get_connection(self):
        """获取DB连接对象"""
        raise NoImplementException()

    def execute_many(self, sql, args):
        """批量执行SQL语句"""
        raise NoImplementException()

    def fetchall(self, sql, args=None):
        """查询所有数据"""
        raise NoImplementException()

    def fetchone(self, sql, args=None):
        """查询单条数据"""
        raise NoImplementException()


class DatabaseBase(IBase):
    """数据库操作类"""

    def __init__(
            self,
            host="localhost",
            port=3306,
            username="root",
            password="root",
            database="",
            charset="utf8mb4",
    ):
        """
        创建数据库连接对象的初始化方法
        @param host 数据库主机地址
        @param port 数据库端口号
        @param username 用户名
        @param password 密码
        @param database 数据库
        @param charset 字符集
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.charset = charset
        self.connection = self.get_connection()
        self.__re_connect_time = 0  # 上次重连的时间

    def get_connection(self, is_reconnect=False):
        """
        获取连接对象
        :param is_reconnect 是否尝试重连
        """
        logger.debug(
            "尝试与MySQL建立连接",
            host=self.host,
            port=self.port,
            username=self.username,
            database=self.database,
        )
        connection = None
        range_num = 6 if is_reconnect else 2
        for i in range(range_num):
            try:
                if i % 2 == 0:
                    connection = Connection(
                        host=self.host,
                        port=self.port,
                        user=self.username,
                        password=self.password,
                        database=self.database,
                        charset=self.charset,
                        cursorclass=DictCursor,
                    )
                else:
                    connection = Connection(
                        host=self.host,
                        port=self.port,
                        user=self.username,
                        password=self.password,
                        database=self.database,
                        charset=self.charset,
                        cursorclass=DictCursor,
                        ssl={"ssl": None}
                    )
                connection.ping()  # cping 校验连接是否异常
                logger.debug(
                    "与MySQL建立连接成功",
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    database=self.database,
                )
                break
            except Exception as e:
                logger.error(
                    "连接 MySQL 服务失败",
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    database=self.database,
                    error=e,
                )
            time.sleep(1)
        return connection


    def re_connection(self, num=1, stime=1):
        """
        重新连接
        :param num 连接次数
        :param stime 休眠时间
        """
        # 与上次成功重连的时间不要超过10分钟，防止短时间来对MySQL发送太多请求
        if time.time() - self.__re_connect_time < 60 * 10:
            return

        # 如果连接正常，则不执行重连
        if self.is_connected():
            return

        # 尝试重新连接
        _number = 0
        while _number <= num:
            try:
                self.connection.ping()  # cping 校验连接是否异常
                logger.debug(
                    "重新连接MySQL成功",
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    database=self.database,
                )
                break
            except Exception as e:
                logger.error(
                    f"连接 MySQL 服务失败，{stime} 秒后尝试重新连接",
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    database=self.database,
                    error=e,
                )
                self.connection = self.get_connection()
                if self.is_connected():  # 重新连接成功
                    self.__re_connect_time = time.time()  # 记录重连时间
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束


    def is_connected(self):
        """查看是否能够正常连接"""
        try:
            self.connection.ping()  # cping 校验连接是否异常
            return True
        except Exception as e:
            logger.error(
                "连接 MySQL 服务失败",
                host=self.host,
                port=self.port,
                username=self.username,
                database=self.database,
                error=e,
            )
            return False


    def execute(self, sql_str, args=None):
        """执行SQL语句"""
        logger.debug("准备执行SQL语句", sql=sql_str, args=args)
        if sql_str is None:
            return

        # 执行重连
        self.re_connection()

        # 执行SQL语句
        for i in range(3):
            cursor = self.connection.cursor()
            try:
                # 执行 SQL 语句并提交事务
                if args:
                    cursor.execute(sql_str, args)
                else:
                    cursor.execute(sql_str)
                self.connection.commit()
                logger.debug("成功执行SQL语句", sql=sql_str, args=args)
                break
            except Exception as e:
                logger.error(
                    "执行SQL语句失败",
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    database=self.database,
                    sql=sql_str,
                    args=args,
                    error=e,
                )
                # 出错后回滚事务
                self.connection.rollback()
                # 尝试重新获取连接
                self.connection = self.get_connection()
                raise e
            finally:
                # 关闭连接
                cursor.close()
            time.sleep(i ** 2)


    def execute_many(self, sql, args):
        """
        批量执行SQL语句
        sql: 要执行的SQL语句
        args：要求是一个嵌套数据类型
        """
        logger.debug("准备批量执行SQL语句", sql=args, args=args)

        # 执行重连
        self.re_connection()

        # 获取连接
        cursor = self.connection.cursor()
        try:
            # 执行 SQL 语句并提交事务
            if args:
                cursor.executemany(sql, args)
            else:
                cursor.executemany(sql)
            self.connection.commit()
            logger.debug("成功批量执行SQL语句", sql=sql, args=args)
        except Exception as e:
            logger.error(
                "批量执行SQL语句失败",
                host=self.host,
                port=self.port,
                username=self.username,
                database=self.database,
                sql=sql,
                args=args,
                error=e,
            )
            # 出错后回滚事务
            self.connection.rollback()
            raise e
        finally:
            # 关闭连接
            cursor.close()


    def fetchall(self, sql, args=None):
        """执行查询所有数据"""
        logger.debug("准备通过SQL查询数据", sql=sql, args=args)

        # 执行重连
        self.re_connection()

        # 执行查询
        with self.connection.cursor() as cursor:
            try:
                # 执行查询，提交事务，返回结果
                if args:
                    cursor.execute(sql, args)
                else:
                    cursor.execute(sql)
                result = cursor.fetchall()
                logger.debug("成功通过SQL查询数据", sql=sql, args=args)
                return result
            except Exception as e:
                logger.error(
                    "执行SQL语句查询失败",
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    database=self.database,
                    sql=sql,
                    args=args,
                    error=e,
                )
                raise e
            finally:
                # 关闭连接
                cursor.close()


    def fetchone(self, sql, args=None):
        """执行查询所有数据"""
        logger.debug("准备通过SQL查询单条数据", sql=sql, args=args)

        # 执行重连
        self.re_connection()

        # 执行查询
        with self.connection.cursor() as cursor:
            try:
                # 执行查询，提交事务，返回结果
                cursor.execute(sql, args)
                result = cursor.fetchone()
                logger.debug("成功通过SQL查询单条数据", sql=sql, args=args, result=result)
                return result
            except Exception as e:
                logger.error(
                    "执行SQL语句单个查询失败",
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    database=self.database,
                    sql=sql,
                    args=args,
                    error=e,
                )
                raise e
            finally:
                # 关闭连接
                cursor.close()


    def use(self, database):
        """切换数据库"""
        logger.debug("准备切换数据库", old_database=self.database, new_database=database)
        self.database = database
        self.connection = self.get_connection()
        logger.debug("成功切换数据库", new_database=database)
