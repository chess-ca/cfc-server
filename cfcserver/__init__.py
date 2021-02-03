
from . import dao as app_dao
from . import models as app_models
from . import services as app_services

# ---- App Config (set so IDE autocomplete will work
config = app_models.app_config.Development()

# ---- "app.*" is a simple Service Locator
# - Ref: https://en.wikipedia.org/wiki/Service_locator_pattern
# - for testing, override these with mocks as needed
dao = app_dao
models = app_models
services = app_services


class RATINGS_DB(app_dao.databases.RatingsDB):
    DB_CONNECT = config.RATINGS_DB


def initialize(is_prod):
    global config
    if is_prod:
        config = app_models.app_config.Production()
