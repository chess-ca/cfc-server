
import re
from pathlib import Path
import flask as _flask
import codeboy4py.flask.routing as cb4py_routing
from .auth import auth
from cfcserver.models.appconfig import AppConfig

_routing_rules = [
    ('/', 'main.home'),
    ('/si/<action>/', 'auth.signin'),
    ('/jobs/', 'jobs.list'),
    ('/jobs/upload/', 'jobs.upload'),
    ('/jobs/view/<job_name>', 'jobs.view'),
]


def initialize(app):
    ui_html = _flask.Blueprint('ui_html', __name__, template_folder='templates')

    def jinja_built_url(file_path):
        return AppConfig.STATIC_BUILT_URL.format(file_path)
    app.jinja_env.globals['built_url'] = jinja_built_url
    built_dir = get_built_url()
    AppConfig.STATIC_BUILT_URL = f'/static/{built_dir}/{{}}'

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
    return _flask.render_template('home.html')


def get_built_url():
    built_confg_fn = Path(__file__).resolve().parents[2] / 'static-src/built.config.cjs'
    with open(built_confg_fn, 'rt') as bc:
        built_config = str(bc.read())
    pattern = r'dest_dir\s*=\s*["\']([^"\']*)["\']'
    s = re.search(pattern, built_config)
    built_dir = s.group(1) if s else 'NOT_SET'
    return built_dir

