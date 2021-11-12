
import re
import flask as _flask
import codeboy4py.flask.routing as cb4py_routing
from .utils import render_svelte, get_built_url_format
from .auth import auth
from cfcserver.models.appconfig import AppConfig

_routing_rules = [
    ('/', 'main.home'),
    ('/si/<action>/', 'auth.signin'),
    ('/jobs/', 'jobs.job_list'),
    ('/jobs/upload/', 'jobs.job_upload'),
    ('/jobs/view/<job_name>', 'jobs.job_view'),
]


def initialize(app):
    ui_html = _flask.Blueprint('ui_html', __name__, template_folder='templates')

    AppConfig.STATIC_BUILT_URL = get_built_url_format()
    def url_for_built(file_path):
        return AppConfig.STATIC_BUILT_URL.format(file_path)
    app.jinja_env.globals['url_for_built'] = url_for_built

    rd = cb4py_routing.RouteDefiner(ui_html)
    rd.set_rule_prefix('/office')
    rd.set_import_prefix('cfcserver.ui.html.')
    rd.add_url_rules(_routing_rules)

    app.register_blueprint(ui_html)
    app.jinja_env.add_extension('jinja2.ext.do')

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render('hdr/page_not_found.html'), 404


@auth
def home():
    return render_svelte('Home')
