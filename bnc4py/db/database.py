# ======================================================================
# db/database.py
#   - Database objects with (opinionated) helper methods.
# ======================================================================

import dataclasses as dc
import sqlite3, configparser
from pathlib import Path


# ----------------------------------------------------------------------
# GenericDatabase:
# ----------------------------------------------------------------------
class GenericDatabase:
    db_connect = None

    def __init__(self):
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
            self._dbcon.close()

    # -------- Cursor Methods
    def create_tables(self):
        pass

    def create_indices(self):
        pass

    # -------- Cursor Methods
    # TODO: Don't be inconsistent with sqlite3 methods
    #  - Ref: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchall
    def fetchone(self, sql, sqldata=None):
        self._dbcsr = self.dbcon().cursor()
        self._dbcsr.execute(sql, sqldata)
        row = self._dbcsr.fetchone()
        return row

    def fetchrows(self, sql, sqldata=None):
        self._dbcsr = self.dbcon().cursor()
        rowset = self._dbcsr.execute(sql, sqldata)
        return rowset

    def execute(self, sql, sqldata=None):
        self._dbcsr = self.dbcon().cursor()
        if sqldata is None:
            self._dbcsr.execute(sql)
        else:
            self._dbcsr.execute(sql, sqldata)
        self._rowcount = self._dbcsr.rowcount
        return self._rowcount

    def executemany(self, sql, sqldata=None):
        self._dbcsr = self.dbcon().cursor()
        if sqldata is None:
            self._dbcsr.executemany(sql)
        else:
            self._dbcsr.executemany(sql, sqldata)
        self._rowcount = self._dbcsr.rowcount
        return self._rowcount

    # -------- Connection Methods
    def commit(self):
        if self._dbcon:
            self._dbcon.commit()

    def rollback(self):
        if self._dbcon:
            self._dbcon.rollback()

    def rowcount(self):
        return self._rowcount

    # -------- Helper Methods
    def row_to_dataclass(self, row, dataclazz, rename=None, skip=None):
        # Converts a database row to a Python dataclass.
        #  - row: A row from the database.
        #  - dataclazz: A class that was decorated with @dataclass.
        #  - rename: Map of database-column-name ==> dataclass-attr-name.
        #  - skip: List of dataclass-attr-names to exclude.
        dc2col_rename = {} if not rename \
            else {rename[col_name]: col_name for col_name in rename}
        skip = skip or []
        row_col_list = [col[0] for col in self._dbcsr.description]
        dc_attr_list = [f.name for f in dc.fields(dataclazz)]

        dc_attributes = dict()
        for dc_attr in dc_attr_list:
            if dc_attr in skip:
                continue
            row_col = dc2col_rename.get(dc_attr, dc_attr)
            if row_col in row_col_list:
                dc_attributes[dc_attr] = row[row_col]
        dataclazz_instance = dataclazz(**dc_attributes)
        return dataclazz_instance

    def describe_row(self):
        return [col[0] for col in self._dbcsr.description]


# ----------------------------------------------------------------------
# SqliteDB:
# ----------------------------------------------------------------------
class SqliteDB(GenericDatabase):
    # ---- Connect to an SQLite database (using self.db_connect)
    def dbcon(self) -> sqlite3.Connection:
        if self._dbcon is None:
            if not isinstance(self.db_connect, dict):
                self.db_connect = dict(database=self.db_connect)
            self._dbcon = sqlite3.connect(**self.db_connect)
            self._dbcon.row_factory = sqlite3.Row
        return self._dbcon


# ----------------------------------------------------------------------
# VersionedSqliteDB:
#   - SQLite database with a version number in the database's file name.
#   - Enables keeping the "active" version available while the next
#     version is being created & loaded. After, the switch can be made.
#   - Directory "db_directory" contains all versions of the database
#     and "<db_prefix>.state.ini" with the active & next version numbers.
# ----------------------------------------------------------------------
class VersionedSqliteDB(SqliteDB):
    db_directory = None
    db_prefix = None
    db_suffix = 'sqlite'

    def __init__(self, open_next_version=False):
        assert self.db_directory, 'Subclasses must override "db_directory"'
        assert self.db_prefix, 'Subclasses must override "db_prefix"'
        self.open_next_version = open_next_version
        self.db_version_number = -1
        self.db_fpath = None
        fp = Path(self.db_directory, f'{self.db_prefix}.state.ini')
        if not fp.exists():
            raise FileNotFoundError(f'Database state file not found: {fp}')
        self.db_state_fpath = fp
        super().__init__()

    def dbcon(self):
        if self.db_fpath is None:
            state_ini = str(self.db_state_fpath)
            cp = configparser.ConfigParser()
            cp.read(state_ini)
            if not self.open_next_version:
                version = int(cp['version']['active'])
            else:
                version = int(cp['version']['next_unused'])
                cp['version']['next_unused'] = str(version + 1)
                with open(state_ini, 'w') as state_ini_f:
                    cp.write(state_ini_f)
            self.db_version_number = version
            db_fname = f'{self.db_prefix}.{version:04}.{self.db_suffix}'
            self.db_fpath = Path(self.db_directory, db_fname)

        if self._dbcon is None:
            if isinstance(self.db_connect, dict):
                # keep other connection args, if specified.
                self.db_connect['database'] = self.db_fpath
            else:
                self.db_connect = dict(database=self.db_fpath)
            self._dbcon = super().dbcon()
        return self._dbcon

    def make_this_db_active(self):
        state_ini = str(self.db_state_fpath)
        cp = configparser.ConfigParser()
        cp.read(state_ini)
        cp['version']['active'] = str(self.db_version_number)
        with open(state_ini, 'w') as state_ini_f:
            cp.write(state_ini_f)


# ----------------------------------------------------------------------
# MockDB:
# ----------------------------------------------------------------------
class MockDB(GenericDatabase):
    MOCK_FETCHONE = None
    MOCK_FETCHROWS = []

    def fetchone(self, sql, sqldata=None):
        self._rowcount = 1
        return self.MOCK_FETCHONE

    def fetchrows(self, sql, sqldata=None):
        self._rowcount = len(self.MOCK_FETCHROWS)
        return self.MOCK_FETCHROWS

    def commit(self):
        pass

    def rollback(self):
        pass
