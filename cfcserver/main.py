
import logging, sys
from cfcserver.models.appconfig import AppConfig
from cfcserver import gateways


def initialize(app_config_file):
    AppConfig.init_appconfig(app_config_file)
    gateways.initialize(AppConfig)
    _logging_setup()


def _logging_setup():
    log = logging.getLogger('cfcserver')
    log.setLevel(logging.INFO)
    log_format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_format)
    log.addHandler(log_handler)
