
import flask as _flask
from flask_cors import CORS
import codeboy4py.flask.routing as cb4py_routing

_routing_rules = (
    # -------- Version 0 (initial)
    ('SET_URL_PREFIX', '/api/ratings'),
    ('SET_IMPORT_PREFIX', 'cfcserver.ui.api.ratings.'),
    ('/player/find', 'player.find'),
    # ('/player/prov/<prov>', 'player.province'),
    ('/player/<int:mid>', 'player.get_details'),
    ('/tournament/<int:tid>', 'tournament.get_details'),
    ('/tournament/find', 'tournament.find'),
    ('/tournament/days/<int:days>', 'tournament.days'),
    ('/tournament/year/<int:year>', 'tournament.year'),

    # -------- Version 1
    ('SET_URL_PREFIX', '/api/cfcdb'),
    ('SET_IMPORT_PREFIX', 'cfcserver.ui.api.'),
    ('/player/v1/top', 'player.find_top_players_v1'),
    # ('/player/v1/find', 'player.find'),
    # ('/player/prov/<prov>', 'player.province'),
    # ('/player/<int:mid>', 'player.get_details'),
    # ('/tournament/<int:tid>', 'tournament.get_details'),
    # ('/tournament/find', 'tournament.find'),
    # ('/tournament/days/<int:days>', 'tournament.days'),
    # ('/tournament/year/<int:year>', 'tournament.year'),
)


def initialize(app):
    ui_api = _flask.Blueprint('ui_api', __name__)
    CORS(ui_api)
    cb4py_routing.RouteDefiner.add_rules(ui_api, _routing_rules)
    app.register_blueprint(ui_api)
