
import flask as _flask
from flask_cors import CORS
import codeboy4py.flask.routing as cb4py_routing

_routing_rules = (
    # -------- v1 APIs
    ('SET_URL_PREFIX', '/api'),
    ('SET_IMPORT_PREFIX', 'cfcserver.ui.api.'),
    ('/player/v1/find', 'player.find_v1'),
    ('/player/v1/<cfc_id>', 'player.get_details_v1'),
    ('/player/v1/top', 'player.find_top_players_v1'),
    ('/event/v1/find', 'event.find_v1'),
    ('/event/v1/<event_id>', 'event.get_details_v1'),
)


def initialize(app):
    ui_api = _flask.Blueprint('ui_api', __name__)
    CORS(ui_api)
    cb4py_routing.RouteDefiner.add_rules(ui_api, _routing_rules)
    app.register_blueprint(ui_api)
