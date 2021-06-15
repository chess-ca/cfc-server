
import flask as _flask
import codeboy4py.flask.routing as cb4py_routing


def initialize(app):
    ui_api = _flask.Blueprint('ui_api', __name__)

    rd = cb4py_routing.RouteDefiner(ui_api)
    rd.set_rule_prefix('/api/ratings')
    rd.set_import_prefix('cfcserver.ui.api.ratings.')
    rd.add_url_rules([
        ('/player/find', 'player.find'),
        # ('/player/prov/<prov>', 'player.province'),
        ('/player/<int:mid>', 'player.get_details'),
        ('/tournament/<int:tid>', 'tournament.get_details'),
        ('/tournament/find', 'tournament.find'),
        ('/tournament/days/<int:days>', 'tournament.days'),
        ('/tournament/year/<int:year>', 'tournament.year'),
    ])

    app.register_blueprint(ui_api)
