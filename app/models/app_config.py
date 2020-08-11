
import configparser, pathlib
import bnc4py.py.config as bnc_config

_root_dir = pathlib.Path(__file__).parents[2]
_app_config_file = str(_root_dir / 'private' / 'config' / 'app.config')


class BaseConfig(bnc_config.BaseConfig):
    BNC_CONFIG_CONFIGPARSER_FILES =  _app_config_file

    ROOT_DIR = str(_root_dir)
    CONFIG_DIR = str(_root_dir / 'private' / 'config')
    DATA_DIR = str(_root_dir / 'private' / 'data')

    RATINGS_DB = str(_root_dir / 'private' / 'data' / 'cfc.ratings.sqlite')
    RATINGS_CACHE_MAXAGE = 600


class Development(BaseConfig):
    BNC_CONFIG_CONFIGPARSER_SECTION = 'development'


class Production(BaseConfig):
    BNC_CONFIG_CONFIGPARSER_SECTION = 'production'
