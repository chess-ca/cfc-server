
import flask as _flask
import bnc4py.flask.routing as bnc_routing
from . import ratings

ui_api = _flask.Blueprint('ui_api', __name__)

rd = bnc_routing.RouteDefiner(ui_api)
rd.set_rule_prefix('/api/ratings')
rd.set_import_prefix('ui_api.ratings.')
rd.add_url_rules([
    ('/player/find', 'player.find'),
    # ('/player/prov/<prov>', 'player.province'),
    ('/player/<int:mid>', 'player.get_details'),
    ('/tournament/<int:tid>', 'tournament.get_details'),
    ('/tournament/find', 'tournament.find'),
    ('/tournament/days/<int:days>', 'tournament.days'),
    ('/tournament/year/<int:year>', 'tournament.year'),
])


def initialize(app):
    app.register_blueprint(ui_api)
