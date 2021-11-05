"""
models/appconfig.py
- Container of values and functions required by the app.
- Initialized at start-up. Shared by all requests.
- Should be the only model that is aware of external packages.
"""
from codeboy4py.py.appconfig import AppConfigBase
import codeboy4py.db as cb4py_db
import codeboy4py.db.sqlalchemy as cb4py_sqla


class AppConfig(AppConfigBase):
    _CB4PY_DEFAULT_LOGGER = 'cfcserver'

    CONFIG_FILE: str = ''
    # -------- Environment: defined in the CONFIG_FILE
    ENV: str = ''               # production | development
    CONFIG_DIR: str = ''
    DATA_DIR: str = ''
    JOBS_DIR: str = ''
    FILES_DIR: str = ''
    AUTH_GOOGLE_CLIENT_ID = ''
    AUTH_GOOGLE_CLIENT_SECRET = ''
    AUTH_EMAILS = ''

    # -------- UI Config
    RATINGS_CACHE_MAXAGE: str = '600'

    # -------- App Config
    CFCDB: cb4py_sqla.VersionedSQLiteDB
    RATINGS_AUDIT_EXTRACT_FILE: str

    STATIC_BUILT_URL: str = '/static/built.unset/{}'

    # @@@@@@@@@@@@@@@@@@@ TODO: V2-Deprecate
    dao = None
    models = None
    services = None

    # @@@@@@@@@@@@@@@@@@@ TODO: Deprecate
    class RATINGS_DB(cb4py_db.VersionedSqliteDB):
        db_prefix = 'ratings'
        db_directory = None     # set in initialize()

    @classmethod
    def init_appconfig(cls, app_config_file):
        cls.init_logger('cfcserver', level='DEBUG')

        cls.CONFIG_FILE = app_config_file
        cls.init_from_config_file(app_config_file, 'cfcserver', required=[
            'ENV', 'CONFIG_DIR', 'DATA_DIR', 'JOBS_DIR', 'FILES_DIR',
            'AUTH_GOOGLE_CLIENT_ID', 'AUTH_GOOGLE_CLIENT_SECRET',
            'AUTH_EMAILS',
        ])

        cls.CFCDB = cb4py_sqla.VersionedSQLiteDB(
            prefix='cfcdb',
            directory=cls.DATA_DIR + '/cfcdb',
        )
