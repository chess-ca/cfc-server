
from codeboy4py.py.config import get_config_section


class GatewayConfig:
    DS_RATINGS_DIR: str


def initialize(AppConfig):
    GC = GatewayConfig
    config = get_config_section(AppConfig.APP_CONFIG_FILE, 'cfcserver')

    # ---- ds_ratings:
    GC.DS_RATINGS_DIR = config.get('DS_RATINGS_DIR', f'{AppConfig.DATA_DIR}/ratings')
