
from typing import Dict, Tuple
from atom_bk_frame.db.db_accesors.query_factory import MysqlQueryFactory
from atom_bk_frame.db.db_drivers.db_driver import DbDriver
from atom_bk_frame.util.settings_util import get_member_by_settings
import mysql.connector as mysql
from mysql.connector import (connection)


class MySqlDriver(DbDriver):
    DB_CONFIG_SETTING_NAME = "DB_CONFIG"

    connector: connection.MySQLConnection = None

    def __enter__(self,):
        self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def get_query_factory(self) -> MysqlQueryFactory:
        return MysqlQueryFactory()

    def connect(self, is_transaction=False):
        db_config = get_member_by_settings(self.DB_CONFIG_SETTING_NAME)

        if not db_config:
            raise Exception('not exist db config')

        self.connector = mysql.connect(**db_config)
        self.connector.autocommit = not is_transaction

    def disconnect(self,):
        self.connector.close()

    def commit(self,):
        self.connector.commit()

    def rollback(self):
        self.connector.rollback()

    def is_connect(self,) -> bool:
        if not self.connector:
            return False
        return self.connector.is_connected()

    def fetch(self, query: str) -> Dict:
        cur = self.connector.cursor(dictionary=True)

        cur.execute(query)
        rows = cur.fetchall()
        return rows

    def fetch_with_param(self, query: str, param: Tuple) -> Dict:

        cur = self.connector.cursor(dictionary=True)

        cur.execute(query, param)
        rows = cur.fetchall()
        return rows

    def execute(self, query: str, param) -> int:
        cur = self.connector.cursor()
        cur.execute(query, param)

        return cur.lastrowid

    def execute_bulk(self, query: str, param) -> int:
        cur = self.connector.cursor()
        cur.execute(query, param)

        return cur.rowcount
