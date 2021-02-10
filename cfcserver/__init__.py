
import os, sys, logging
import bnc4py.db as bnc4py_db
from pathlib import Path
from . import dao as app_dao
from . import models as app_models
from . import services as app_services

# ---- App Config (set so IDE autocomplete will work
config = app_models.app_config.Development()

log = logging.getLogger('main')
log.setLevel(logging.INFO)
log_format = logging.Formatter("%(asctime)s: %(message)s")
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(log_format)
log.addHandler(log_handler)

# ---- "app.*" is a simple Service Locator
# - Ref: https://en.wikipedia.org/wiki/Service_locator_pattern
# - for testing, override these with mocks as needed
dao = app_dao
models = app_models
services = app_services


# class RATINGS_DB(app_dao.databases.RatingsDB):
#     db_connect = config.RATINGS_DB
class RATINGS_DB(bnc4py_db.VersionedSqliteDB):
    db_prefix = 'ratings'
    db_directory = Path(os.environ['APP_DATA_DIR'], 'ratings')


# class RATINGS_DB_V2(bnc4py_db.VersionedSqliteDB):
#     db_prefix = 'ratings'
#     db_directory = Path(os.environ['APP_DATA_DIR'], 'ratings')


def initialize(is_prod):
    global config
    if is_prod:
        config = app_models.app_config.Production()
