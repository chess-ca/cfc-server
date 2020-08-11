
import flask as _flask
import bnc4py.flask.routing as bnc_routing

ui_html = _flask.Blueprint('ui_html', __name__)

rd = bnc_routing.RouteDefiner(ui_html)
rd.set_rule_prefix('/biz')
rd.set_import_prefix('ui_html.')
rd.add_url_rules([
])


def initialize(app):
    app.register_blueprint(ui_html)
    app.jinja_env.add_extension('jinja2.ext.do')

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render('hdr/page_not_found.html'), 404
