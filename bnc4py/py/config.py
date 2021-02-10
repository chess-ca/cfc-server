# ======================================================================
# py/config.py - Configuration Helper
# ======================================================================
import configparser

class BaseConfig:
    BNC_CONFIG_CONFIGPARSER_FILES = None
    BNC_CONFIG_CONFIGPARSER_SECTION = None

    def __init__(self):
        if self.BNC_CONFIG_CONFIGPARSER_FILES:
            self._bnc_overwrite_attrs_with_values_from_config_files()

    def _bnc_overwrite_attrs_with_values_from_config_files(self):
        cp = configparser.ConfigParser()
        cp.read(self.BNC_CONFIG_CONFIGPARSER_FILES)
        if not cp.has_section(self.BNC_CONFIG_CONFIGPARSER_SECTION):
            raise Exception('BNC0000: Config is missing section "{}". Files: {}'.format(
                self.BNC_CONFIG_CONFIGPARSER_SECTION, self.BNC_CONFIG_CONFIGPARSER_FILES
            ))
        cs = cp[self.BNC_CONFIG_CONFIGPARSER_SECTION]
        for key in cs:
            key = key.upper()   # for overrides, keys must be upper case!
            if not hasattr(self, key):
                raise Exception('BNC0000: Config has unknown key "{}" (a typo?). Section "{}"; files: {}'.format(
                    key, self.BNC_CONFIG_CONFIGPARSER_SECTION, self.BNC_CONFIG_CONFIGPARSER_FILES
                ))
            setattr(self, key, cs[key])
