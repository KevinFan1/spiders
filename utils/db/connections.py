import threading

import pymysql


class DBConnector:
    _instance = None
    _lock = threading.Lock()
    _conn = None

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls, *args, **kwargs)
            return cls._instance

    def __init__(self):
        pass

    @property
    def connection(self):
        if not self._conn:
            self._conn = pymysql.connect(
                user='root',
                password='',
                host='127.0.0.1',
                port=3306,
                database='test'
            )
        return self._conn

    def query(self, sql: str):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, args=(1,))
            return cursor.fetchall()


if __name__ == '__main__':
    conn1 = DBConnector()
    conn2 = DBConnector()

    print(conn1.query('select * from user where id=%s'))
    print(conn2.query('select * from user where id=%s;'))
