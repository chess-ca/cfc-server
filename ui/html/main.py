
import flask as _flask
import codeboy4py.flask.routing as cb4py_routing


def initialize(app):
    ui_html = _flask.Blueprint('ui_html', __name__)

    rd = cb4py_routing.RouteDefiner(ui_html)
    rd.set_rule_prefix('/biz')
    rd.set_import_prefix('ui.html.')
    rd.add_url_rules([
        # ('/foo/find', 'foo.find'),
    ])

    app.register_blueprint(ui_html)
    app.jinja_env.add_extension('jinja2.ext.do')

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render('hdr/page_not_found.html'), 404
