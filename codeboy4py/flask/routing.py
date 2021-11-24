
import importlib


# ----------------------------------------------------------------------
class RouteDefiner:
    """
    Reduces repetition & boilerplate when defining routes for Flask.
    Set app/blueprint, rule prefix, import prefix just once and they
    will be applied to subsequent .add_url_rule() invocations.
    ALSO, lazy import of handlers (so the entire app need not be loaded
    and initialized during start-up or the 1st request).
    """
    @staticmethod
    def add_rules(flask_app_or_blueprint, rule_list):
        """Add Flask URL routing rules. Rules in the list can be:

        - ['SET_URL_PREFIX', '/url/base']
        - ['SET_IMPORT_PREFIX', 'package1.package2.']
        - [ url, import_callable, methods_list=["GET"], endpoint=<calculated>]

        :param flask_app_or_blueprint:
        :param rule_list: List of rules.
        """
        url_prefix = ''
        import_prefix = ''
        for rule in rule_list:
            if rule[0] == 'SET_URL_PREFIX':
                url_prefix = rule[1]
            elif rule[0] == 'SET_IMPORT_PREFIX':
                import_prefix = rule[1]
            else:
                url = url_prefix + rule[0]
                handler = import_prefix + rule[1]
                methods = rule[2] if len(rule) > 2 else ['GET']
                endpoint = rule[3] if len(rule) > 3 \
                        else rule[1].lstrip('.').replace('.', '_')
                flask_app_or_blueprint.add_url_rule(
                    url,
                    endpoint=endpoint,
                    view_func=_LazyView(handler),
                    methods=methods,
                )


class _LazyView:
    # Based on https://flask.palletsprojects.com/en/1.1.x/patterns/lazyloading/
    # but with Werkzeug funcs replaced by Python 3 importlib funcs.
    def __init__(self, import_module_name):
        self.__module__, self.__name__ = import_module_name.rsplit('.', 1)
        self.func = None

    def __call__(self, *args, **kwargs):
        if self.func is None:
            module = importlib.import_module(self.__module__)
            if hasattr(module, self.__name__):
                self.func = getattr(module, self.__name__)
            else:
                raise ImportError(f'Import not found: {self.__module__}.{self.__name__}')
        return self.func(*args, **kwargs)
