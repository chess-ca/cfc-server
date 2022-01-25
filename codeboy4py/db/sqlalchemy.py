"""
Helpers for SQLAlchemy access to databases
"""
from typing import Union, List
import sqlalchemy as sa
import dataclasses as dc
import pathlib, configparser, datetime


class RowToDict:
    """
    Converts SQLAlchemy Rows to a Python dicts

    - Only the specified columns are included in the dict
      (to omit columns that should be excluded).
    - Can rename database columns to different dict keys.
    - Can get a list of SQLAlchemy columns for use in `select(...)`
      (to minimize the data fetched from the database).
    - Should pre-define it once; then re-use in many requests.
    """
    def __init__(self,
            include: Union[List[str], str, None] = None,
            rename: Union[dict, None] = None,
            table: Union[sa.Table, None] = None,
    ):
        """
        :param include: list of row cols to be included
            (can be a list or a space-separated string)
        :param rename: map of database column names to dict keys
        :param table: SQLAlchemy Table from which to get a subset
            of its columns for use in `select(...)`.
        """
        self._include = include if isinstance(include, list) \
            else str(include).split() if isinstance(include, str) \
            else '*'    # Default: include all row fields.
        self._rename = rename or {}
        if table is None:
            self._cols = None
        elif self._include == '*':
            self._cols = list(table.c)
        else:
            self._cols = [getattr(table.c, col)
                for col in self._include
                if hasattr(table.c, col)
            ]

    def to_dict(self, row: sa.engine.Row) -> dict:
        """
        Convert a SQLAlchemy row to a dict with only the included columns
        (with renaming of columns to keys as specified).

        - row._asdict() can be used instead (with slightly better performance
          but slightly less future-proof) if this converter was instantiated
          with a table, this.get_cols() was used in the select(...), and
          no columns need to be renamed. In this case, the row will already
          have only the needed columns with the correct names.

        :param row: an SQLAlchemy row
        """
        a_dict = {}
        for col in row._fields:
            if self._include == '*' or col in self._include:
                key = self._rename.get(col, col)
                a_dict[key] = getattr(row, col)
        return a_dict

    def get_cols(self) -> list:
        return self._cols


class RowToDataclass:
    """
    Convert an SQLAlchemy database row to a Python dataclass.
     - Row may have only a subset of the table's columns so
       columns not in the row are auto-skipped.
     - Initialize once then re-use many times (for performance)
    """
    def __init__(self, dataclass: dc.dataclass, rename=None, skip=None):
        """
        :param dataclass: a Python class decorated with @dataclass
        :param rename: Map of database-column-name -> dataclass-attr-name
        :param skip: List of dataclass-attr-names to exclude
        """
        self._dataclass = dataclass
        attr_to_col_rename = {} if rename is None \
            else {attr: col for col, attr in rename.items()}
        self._col_to_attr = {}
        for attr in self._dataclass._fields:
            if skip is None or attr not in skip:
                col = attr_to_col_rename.get(attr, attr)
                self._col_to_attr[col] = attr

    def to_dataclass(self, row: sa.engine.Row):
        """Convert row (from SQLAlchemy) to dataclass (app's models)"""
        attributes = {}
        for col, attr in self._col_to_attr.items():
            if hasattr(row, col):   # row may have only a subset of columns
                attributes[attr] = getattr(row, col)
        return self._dataclass(**attributes)


def dataset(*col_definitions):
    columns = []
    for cd in col_definitions:
        if not isinstance(cd, (list, tuple,)):
            columns.append(cd)
        else:
            include = cd[1] if isinstance(cd[1], (list, tuple)) \
                else cd[1].split()
            for name, col in cd[0].columns.items():
                if name in include:
                    columns.append(col)
    return columns


class VersionedSQLiteDB:
    """

    """
    max_engine_age = 60*60*3    # recycle engine after 3 hours

    def __init__(self,
            directory: str,     # location of the .sqlite file and its state .ini file
            prefix: str,        # prefix in file name of the .sqlite and .ini files
            echo: bool = False, # for create_engine(), for debugging.
    ):
        self.directory = directory
        self.prefix: str = prefix
        self._echo = echo
        ini_file = pathlib.Path(directory, prefix + '.state.ini')
        if not ini_file.exists():
            raise FileNotFoundError(f'Versioned database: state file not found: {ini_file}')
        self.state_ini_file = str(ini_file)
        self.engines: dict[int, dict] = {}

    # ---- Methods for version number (stored in .ini file)
    def get_active_version(self):
        # (do not cache this; else manual changes to .state.ini will be ignored)
        cp = configparser.ConfigParser()
        cp.read(self.state_ini_file)
        return int(cp['version']['active'])

    def set_active_version(self, version):
        cp = configparser.ConfigParser()
        cp.read(self.state_ini_file)
        cp['version']['active'] = str(version)
        with open(self.state_ini_file, 'w') as state_ini_f:
            cp.write(state_ini_f)

    def get_next_unused_version(self):
        cp = configparser.ConfigParser()
        cp.read(self.state_ini_file)
        next_unused_version = int(cp['version']['next_unused'])
        cp['version']['next_unused'] = str(next_unused_version + 1)
        with open(self.state_ini_file, 'w') as state_ini_f:
            cp.write(state_ini_f)
        return next_unused_version

    # ---- Methods for SQLAlchemy entities
    def get_engine(self, version=None):
        v = version if version is not None \
            else self.get_active_version()
        self._release_stale_engines()
        now = datetime.datetime.utcnow()
        if v not in self.engines:
            url = 'sqlite:///{}/{}.{:04}.sqlite'.format(
                self.directory, self.prefix, v)
            engine = sa.create_engine(url, future=True, echo=self._echo)
            self.engines[v] = {'engine': engine}
        self.engines[v]['last_ref'] = now
        return self.engines[v]['engine']

    def connect(self, version=None) -> sa.engine.Connection:
        engine = self.get_engine(version=version)
        return engine.connect()

    def begin(self, version=None) -> sa.engine.Connection:
        engine = self.get_engine(version=version)
        return engine.begin()

    def _release_stale_engines(self):
        # Otherwise a long running server will have many engines cached.
        now = datetime.datetime.utcnow()
        for v in self.engines:
            age_s = (now - self.engines[v]['last_ref']).total_seconds()
            if age_s > self.max_engine_age:
                del self.engines[v]
