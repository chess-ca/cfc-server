# ======================================================================
# py/config.py - Configuration Helper
# ======================================================================
import configparser, os.path


def get_config_section(config_file, config_section):
    if not os.path.isfile(config_file):
        raise Exception('CB4PY0000: Config file not found: ' + config_file)
    cp = configparser.ConfigParser()
    cp.read(config_file)
    if not cp.has_section(config_section):
        raise Exception('CB4PY0000: Missing section "{}" in config file {}'
            .format(config_section, config_file))
    return cp[config_section]


def set_from_config_file(clazz, config_file, config_section, required_vars):
    config = get_config_section(config_file, config_section)
    for var in required_vars:
        if var not in config:
            raise KeyError('Var "{}" not found in section "{}" of config file {}'
                .format(var, config_section, config_file))
        setattr(clazz, var, config[var])



class AppConfigBase:
    @classmethod
    def set_from_config_ini(cls, config_file, config_section, required):
        pass

    @classmethod
    def get(cls, attr_name, default=None, substitions=True):
        if not hasattr(cls, attr_name):
            raise ValueError('CB4PY0000: App config missing attribute: ' + attr_name)
        attr_value = getattr(cls, attr_name, default)
        if substitions and isinstance(attr_value, str):
            levels = 5
            while levels > 0 and '{' in attr_value:
                attr_value = attr_value.format(**cls.__dict__)
                levels -= 1
        return attr_value

    @classmethod
    def load_from_ini(self, ini_file, ini_section):
        if not os.path.isfile(ini_file):
            raise FileNotFoundError('CB4PY0000: App config file not found: ' + ini_file)


class Registry:
    # Ref: https://martinfowler.com/eaaCatalog/registry.html ; aka Service Locator
    # PRO: Decoupled so can replace with mocks when testing
    # CON: Must register all; so must import & initialize all. :(
    # CON: Decoupled means IDE cannot autocomplete
    CB4PY_REGISTRY = dict()

    @classmethod
    def register(cls, component_id, component):
        cls.CB4PY_REGISTRY[component_id] = component

    @classmethod
    def get(cls, component_id):
        if component_id not in cls.CB4PY_REGISTRY:
            raise Exception('CB4PY0000: Component "{}" was not found in AppConfig registry.'.format(component_id))
        return cls.CB4PY_REGISTRY[component_id]
