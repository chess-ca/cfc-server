
import app.dao
import app.models
import app.services

# ---- App Config (set so IDE autocomplete will work
config = app.models.app_config.Development()

# ---- Simple Locator (for testing, override thes with mocks as needed)
dao = app.dao
models = app.models
services = app.services


class RATINGS_DB(app.dao.databases.RatingsDB):
    DB_CONNECT = config.RATINGS_DB


def initialize(is_prod):
    global config
    if is_prod:
        config = app.models.app_config.Production()
