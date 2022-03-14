
from .create import *
from cfcserver import AppConfig


def get_dbcon():
    return AppConfig.CFCDB.connect()
