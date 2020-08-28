
import os
from pathlib import Path
import bnc4py.py.config as bnc_config

_root_dir = Path(__file__).parents[2]
_app_config_dir = Path(os.environ['APP_CONFIG_DIR'])
_app_data_dir = Path(os.environ['APP_DATA_DIR'])


class BaseConfig(bnc_config.BaseConfig):
    BNC_CONFIG_CONFIGPARSER_FILES = str(_app_config_dir / 'app.config')

    ROOT_DIR = str(_root_dir)
    CONFIG_DIR = str(_app_config_dir)
    DATA_DIR = str(_app_data_dir)

    RATINGS_DB = str(_app_data_dir / 'cfc.ratings.sqlite')
    RATINGS_CACHE_MAXAGE = 600


class Development(BaseConfig):
    BNC_CONFIG_CONFIGPARSER_SECTION = 'development'


class Production(BaseConfig):
    BNC_CONFIG_CONFIGPARSER_SECTION = 'production'
