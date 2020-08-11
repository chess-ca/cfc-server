
import logging as log
from werkzeug.utils import import_string, cached_property


# ----------------------------------------------------------------------
class RouteDefiner(object):
    """
    Reduces repetition & boilerplate when defining routes for Flask.
    Set app/blueprint, rule prefix, import prefix just once and they
    will be applied to subsequent .add_url_rule() invocations.
    ALSO, lazy import of handlers (so the entire app need not be loaded
    and initialized during start-up or the 1st request).
    """
    def __init__(self, flask_app_or_blueprint, rule_prefix='', import_prefix=''):
        self.app_or_blueprint = flask_app_or_blueprint
        self.rule_prefix = rule_prefix
        self.import_prefix = import_prefix

    def set_rule_prefix(self, rule_prefix):
        self.rule_prefix = rule_prefix

    def set_import_prefix(self, import_prefix):
        self.import_prefix = import_prefix

    def add_url_rule(self, rule, import_name, endpoint=None, **options):
        """
        :param options: Passed to Werkzeug routing. Most common:
            - methods=['GET','POST'] ; default is ['GET']
        """
        handler = self.import_prefix + import_name
        endpoint = endpoint or import_name.lstrip('.').replace('.', '_')
        self.app_or_blueprint.add_url_rule(
            self.rule_prefix + rule,
            endpoint=endpoint,
            view_func=_LazyView(handler),
            **options
        )
        # NOTE: For endpoint, cannot have "."; Flask will auto-prepend blueprint name.

    def add_url_rules(self, rule_list):
        # rule = (rule_url, import_name[, methods])
        _GET = ['GET']
        for rule in rule_list:
            self.add_url_rule(
                rule=rule[0],
                import_name=rule[1],
                methods=rule[2] if len(rule) > 2 else _GET
            )


# ----------------------------------------------------------------------
class _LazyView(object):
    """Ref: https://flask.palletsprojects.com/en/1.1.x/patterns/lazyloading/"""
    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)