#!/usr/bin/env python3
from pymysql.connections import Connection

class DBHelper:
    """
    Database operation tool
    """

    def __init__(self, conn: Connection):
        self.conn = conn
        self.cur = self.conn.cursor()

    def _execute(self, sql):
        """ execute sql
        :param sql:
        :return: Returns integer represents rows affected, if any
        """
        rowcount = self.cur.execute(sql)
        self.conn.commit()
        return rowcount

    def insert(self, sql):
        """ execute insert operation
        :return: insert records count
        """
        return self._execute(sql)

    def select(self, sql):
        """ execute select operation
        :return: result data set
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()

        cur.close()
        return res

    def truncate(self, sql):
        """ execute truncate operation
        :return: truncate records count
        """
        return self._execute(sql)

    def execute(self, sql):
        return self._execute(sql)

    def delete(self, sql):
        """ execute delete operation
        :return: delete records count
        """
        return self._execute(sql)

    def executemany(self, sql, dataset):
        """ Execute a multi-row query，improve operational efficiency
        :param sql: sql
        :param dataset: iterator data set
        :return: affected records count
        """
        rowcount = self.cur.executemany(
            sql,
            dataset
        )
        self.conn.commit()
        return rowcount

    def close(self):
        """ after operating database, conn and coursor must be closed
        :return:
        """
        self.cur.close()
        self.conn.close()
