# ======================================================================
# py/config.py - Configuration Helper
# ======================================================================
import configparser, pathlib


def get_config_section(config_file, section):
    if not pathlib.Path(config_file).exists():
        raise Exception('CB4PY0000: App config file not found: ' + config_file)
    cp = configparser.ConfigParser()
    cp.read(config_file)
    if not cp.has_section(section):
        raise Exception('CB4PY0000: Mising section "{}" in config file {}'
            .format(section, config_file))
    return cp[section]


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
