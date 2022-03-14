"""
Helpers for SQLAlchemy access to databases
"""
import sqlalchemy as sa
import pathlib, configparser, datetime


def column_set(*col_definitions):
    """
    Creates a list of columns or column expressions that can be used in `select`:
        select_cols = dataset(...)
        sql = select(*select_cols)...
    :param col_definitions:
     - a column: mytable.c.name
     - a column element: func.upper(mytable.c.name)
       or: mytable.c.first_name + ' ' + mytable.c.last_name
     - a tuple cd where cd[0] is a table and cd[1] is a string of
       space delimited column names: (mytable, 'id name price colour').
       This will be converted into the corresponding column objects.
    :return: a list of columns or column elements.
    """
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
