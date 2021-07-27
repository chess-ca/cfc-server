import sys, os.path, logging, configparser


class AppConfigBase:
    _CB4PY_DEFAULT_LOGGER = None

    @classmethod
    def init_appconfig(cls, *args, **kwargs):
        """Subclasses should override this with custom inits."""
        pass

    @classmethod
    def init_from_dict(cls, a_dict, required=None, optional=None, emsg=None):
        # Initialize from any dict including os.environ
        emsg = emsg or 'Config value "{}" not found in the settings dictionary.'
        for attr in required or []:
            if attr in a_dict:
                setattr(cls, attr, a_dict[attr])
            else:
                raise Exception(emsg.format(attr))
        for attr in optional or []:
            if attr in a_dict:
                setattr(cls, attr, a_dict[attr])

    @classmethod
    def init_from_config_file(cls, file, section, required=None, optional=None):
        # Initialize from any .ini file
        file = str(file)
        if not os.path.isfile(file):
            raise Exception('Config file not found: {}'.format(file))
        cp = configparser.ConfigParser()
        cp.read(file)
        if not cp.has_section(section):
            raise Exception('Section "{}" not found in config file {}'
                .format(section, file))

        emsg = f'Var "{{}}" not found in section "{section}" of config file {file}'
        cls.init_from_dict(cp[section], required, optional, emsg=emsg)

    @classmethod
    def init_logger(cls, name: str, level: str = 'INFO', default=True, format=None, stream=None):
        log = logging.getLogger(name)
        log.setLevel(getattr(logging, level or 'INFO'))
        log_format = logging.Formatter(format or "%(asctime)s %(levelname)s: %(message)s")
        log_handler = logging.StreamHandler(stream or sys.stdout)
        log_handler.setFormatter(log_format)
        log.addHandler(log_handler)
        if default:
            setattr(cls, '_CB4PY_DEFAULT_LOGGER', name)

    @classmethod
    def getLogger(cls, log_name=None) -> logging.Logger:
        log_name = log_name or getattr(cls, '_CB4PY_DEFAULT_LOGGER')
        log = logging.getLogger(log_name) if log_name \
            else logging.getLogger()
        return log

    @classmethod
    def get(cls, attr_name, substitions=True):
        """
        Returns value of an App Config's attribute after (optionally)
        substituting values of other App Config attributes.
        - Example: if ROOT="/path/to/app" and MYFILE="{ROOT}/files/myfile.txt"
          then AppConfig.get('MYFILE') returns "/path/to/app/files/myfile.txt"
        - Disadvantage: attribut names in strings; intellisense won't work.
        """
        if not hasattr(cls, attr_name):
            raise ValueError('Attribute "{}" not found in App Config'.format(attr_name))
        attr_value = getattr(cls, attr_name)
        if substitions and isinstance(attr_value, str):
            levels = 10
            while levels > 0 and '{' in attr_value:
                attr_value = attr_value.format(**cls.__dict__)
                levels -= 1
        return attr_value
