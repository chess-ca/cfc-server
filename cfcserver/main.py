
import logging, sys
import codeboy4py.py.config as cb4py_config
from codeboy4py.py.config import get_config_section
from cfcserver import gateways

# TODO: V2-Deprecate
import codeboy4py.db as cb4py_db
import codeboy4py.db.sqlalchemy as cb4py_sqla


class AppConfig:
    CONFIG_FILE: str = ''
    # -------- Environment: defined in the CONFIG_FILE
    ENV: str = ''               # production | development
    CONFIG_DIR: str = ''
    DATA_DIR: str = ''
    JOBS_DIR: str = ''
    FILES_DIR: str = ''

    # -------- UI Config
    RATINGS_CACHE_MAXAGE: str = '600'

    # -------- App Config
    CFCDB: cb4py_sqla.VersionedSQLiteDB
    RATINGS_AUDIT_EXTRACT_FILE: str


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # TODO: V2-Deprecate
    dao = None
    models = None
    services = None

    # TODO: V2-Deprecate
    class RATINGS_DB(cb4py_db.VersionedSqliteDB):
        db_prefix = 'ratings'
        db_directory = None     # set in initialize()


def initialize(app_config_file):
    AppConfig.CONFIG_FILE = app_config_file
    cb4py_config.set_from_config_file(
        AppConfig, app_config_file, 'cfcserver', required_vars=[
        'ENV', 'CONFIG_DIR', 'DATA_DIR', 'JOBS_DIR', 'FILES_DIR'
    ])
    AppConfig.CFCDB = cb4py_sqla.VersionedSQLiteDB(
        prefix='cfcdb',
        directory=AppConfig.DATA_DIR + '/cfcdb',
    )

    gateways.initialize(AppConfig)
    _logging_setup()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # TODO: V2-Deprecate
    from . import dao as app_dao
    AppConfig.dao = app_dao
    setattr(AppConfig.RATINGS_DB, 'db_directory', AppConfig.DATA_DIR + '/ratings')


def _logging_setup():
    log = logging.getLogger('cfcserver')
    log.setLevel(logging.INFO)
    log_format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_format)
    log.addHandler(log_handler)
