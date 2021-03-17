
import logging, sys
from codeboy4py.py.config import get_config_section
import gateways

# TODO: V2-Deprecate
import codeboy4py.db as cb4py_db

def test_woohoo():
    print('**** TEST from: ', __file__)
    assert 45 == 455


class AppConfig:
    APP_CONFIG_FILE: str = ''
    # -------- Environment Config
    ENV: str = ''
    CONFIG_DIR: str = ''
    DATA_DIR: str = ''
    JOBS_DIR: str = ''
    FILES_DIR: str = ''

    # -------- UI Config
    RATINGS_CACHE_MAXAGE: str = '600'

    # -------- App Config

    # @@@@ TODO: V2-Deprecate
    dao = None
    models = None
    services = None

    class RATINGS_DB(cb4py_db.VersionedSqliteDB):
        db_prefix = 'ratings'
        db_directory = None     # set in initialize()


def initialize(app_config_file):
    AppConfig.APP_CONFIG_FILE = app_config_file
    config = get_config_section(app_config_file, 'cfcserver')
    prefix = 'APP_'
    required = ['APP_ENV', 'APP_CONFIG_DIR', 'APP_DATA_DIR', 'APP_JOBS_DIR', 'APP_FILES_DIR']
    for var in required:
        if var not in config:
            raise Exception(f'FATAL: Config value "{var}" is missing in config file {app_config_file}')
        setattr(AppConfig, var[len(prefix):], config[var])

    gateways.initialize(AppConfig)
    _logging_setup()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # TODO: V2-Deprecate
    from . import dao as app_dao
    from . import models as app_models
    from . import services as app_services
    AppConfig.dao = app_dao
    AppConfig.models = app_models
    AppConfig.services = app_services
    setattr(AppConfig.RATINGS_DB, 'db_directory', AppConfig.DATA_DIR + '/ratings')


def _logging_setup():
    log = logging.getLogger('main')
    log.setLevel(logging.INFO)
    log_format = logging.Formatter("%(asctime)s: %(message)s")
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_format)
    log.addHandler(log_handler)
