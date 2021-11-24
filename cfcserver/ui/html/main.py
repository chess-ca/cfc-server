
import re
import flask as _flask
from flask_cors import CORS
import codeboy4py.flask.routing as cb4py_routing
from .utils import render_svelte, get_built_url_format
from .auth import auth
from cfcserver.models.appconfig import AppConfig

_routing_rules = (
    ('SET_IMPORT_PREFIX', 'cfcserver.ui.html.'),
    ('SET_URL_PREFIX', '/office'),
    ('/', 'main.home'),
    ('/si/<action>/', 'auth.signin'),

    ('SET_IMPORT_PREFIX', 'cfcserver.ui.html.jobs.'),
    ('SET_URL_PREFIX', '/office/jobs'),
    ('/', 'job_list'),
    ('/upload/', 'job_upload'),
    ('/upload/', 'job_upload_post', ['POST']),
    ('/<job_name>', 'job_view'),
)


def initialize(app):
    ui_html = _flask.Blueprint('ui_html', __name__, template_folder='templates')
    CORS(ui_html)
    cb4py_routing.RouteDefiner.add_rules(ui_html, _routing_rules)

    AppConfig.STATIC_BUILT_URL = get_built_url_format()
    def url_for_built(file_path):
        return AppConfig.STATIC_BUILT_URL.format(file_path)
    app.jinja_env.globals['url_for_built'] = url_for_built

    app.register_blueprint(ui_html)
    app.jinja_env.add_extension('jinja2.ext.do')

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render('hdr/page_not_found.html'), 404


@auth
def home():
    return render_svelte('Home')
