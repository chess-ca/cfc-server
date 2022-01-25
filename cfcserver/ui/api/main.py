
import flask as _flask
from flask_cors import CORS
import codeboy4py.flask.routing as cb4py_routing

_routing_rules = (
    # -------- v0 APIs (deprecating)
    ('SET_URL_PREFIX', '/api/ratings'),
    ('SET_IMPORT_PREFIX', 'cfcserver.ui.api.ratings.'),
    ('/player/find', 'player.find'),                        # TODO: After v1.1: Remove
    # ('/player/prov/<prov>', 'player.province'),
    ('/player/<int:mid>', 'player.get_details'),
    ('/tournament/<int:tid>', 'tournament.get_details'),
    ('/tournament/find', 'tournament.find'),
    ('/tournament/days/<int:days>', 'tournament.days'),
    ('/tournament/year/<int:year>', 'tournament.year'),

    # -------- v1 APIs
    ('SET_URL_PREFIX', '/api'),
    ('SET_IMPORT_PREFIX', 'cfcserver.ui.api.'),
    ('/player/v1/find', 'player.find_v1'),
    ('/player/v1/<cfc_id>', 'player.get_details_v1'),
    ('/player/v1/top', 'player.find_top_players_v1'),
    ('/cfcdb/player/v1/top', 'player.find_top_players_v1', ['GET'], 'old_top_players'),  # TODO: After v1.1: Remove
    # ('/event/v1/find', 'event.find_v1'),
    # ('/event/v1/<event_id>', 'event.get_crosstable_v1'),
)


def initialize(app):
    ui_api = _flask.Blueprint('ui_api', __name__)
    CORS(ui_api)
    cb4py_routing.RouteDefiner.add_rules(ui_api, _routing_rules)
    app.register_blueprint(ui_api)
