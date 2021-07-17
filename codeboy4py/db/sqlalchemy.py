"""
Helpers for SQLAlchemy access to databases
"""
import sqlalchemy as sa
import dataclasses as dc
import pathlib, configparser, datetime


class RowToDataclassConverter:
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


class VersionedSQLiteDB:
    """

    """
    max_engine_age = 60*60*3    # recycle engine after 3 hours

    def __init__(self,
            directory: str,     # location of the .sqlite file and its state .ini file
            prefix: str,        # prefix in file name of the .sqlite and .ini files
    ):
        self.directory = directory
        self.prefix: str = prefix
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
            self.engines[v] = {'engine': sa.create_engine(url, future=True)}
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
