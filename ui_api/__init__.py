
import flask as _flask
import bnc4py.flask.routing as bnc_routing
from . import ratings

ui_api = _flask.Blueprint('ui_api', __name__)

rd = bnc_routing.RouteDefiner(ui_api)
rd.set_rule_prefix('/api/ratings')
rd.set_import_prefix('ui_api.ratings.')
rd.add_url_rules([
    ('/player/find', 'player.find'),
    ('/player/<int:mid>', 'player.get_details'),
    ('/tournament/<int:tid>', 'tournament.get_details'),
])


def initialize(app):
    app.register_blueprint(ui_api)
