"""
PURPOSE: Reduce the boilerplate for the typical use of databases.
"""

import dataclasses as dc
import sqlite3


class Database:
    DB_CONNECT = None

    def __init__(self, connect=None):
        self._dbconnect = connect or self.DB_CONNECT
        self._dbcon = None
        self._dbcsr = None
        self._rowcount = 0

    def dbcon(self):
        return None

    # -------- Context Manager (Python)
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self._dbcon:
            self.dbcon().close()

    # -------- Cursor Methods
    def fetchone(self, sql, sqldata):
        self._dbcsr = self.dbcon().cursor()
        self._dbcsr.execute(sql, sqldata)
        self._rowcount = self._dbcsr.rowcount
        row = self._dbcsr.fetchone()
        return row

    def fetchrows(self, sql, sqldata):
        self._dbcsr = self.dbcon().cursor()
        rowset = self._dbcsr.execute(sql, sqldata)
        self._rowcount = self._dbcsr.rowcount
        return rowset

    # -------- Connection Methods
    def commit(self):
        self.dbcon().commit()

    def rollback(self):
        self.dbcon().rollback()

    def rowcount(self):
        return self._rowcount

    # -------- Helper Methods
    def row_to_dataclass(self, row, dataclazz, rename=None, skip=None):
        dc2row_rename = {} if not rename \
            else {rename[row_name]: row_name for row_name in rename}
        row_keys = [col[0] for col in self._dbcsr.description]
        dc_keys = [f.name for f in dc.fields(dataclazz)]

        dc_fields = dict()
        for dc_key in dc_keys:
            if skip is not None and dc_key in skip:
                continue
            row_key = dc2row_rename.get(dc_key, dc_key)
            if row_key in row_keys:
                dc_fields[dc_key] = row[row_key]
        return dataclazz(**dc_fields)

    def describe_row(self):
        return [col[0] for col in self._dbcsr.description]


class SqliteDB(Database):
    def dbcon(self) -> sqlite3.Connection:
        if self._dbcon is None:
            connect = self._dbconnect if isinstance(self._dbconnect, dict) \
                else dict(database=self._dbconnect)
            self._dbcon = sqlite3.connect(**connect)
            self._dbcon.row_factory = sqlite3.Row
        return self._dbcon


class MockDB(Database):
    MOCK_FETCHONE = None
    MOCK_FETCHROWS = []

    def fetchone(self, sql, sqldata):
        self._rowcount = 1
        return self.MOCK_FETCHONE

    def fetchrows(self, sql, sqldata):
        self._rowcount = len(self.MOCK_FETCHROWS)
        return self.MOCK_FETCHROWS

    def commit(self):
        pass

    def rollback(self):
        pass
