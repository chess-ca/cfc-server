
import flask
from cfcserver import AppConfig
from cfcserver.ui.api.shared import api_response


def find():
    mid = flask.request.args.get('mid', None)
    first = flask.request.args.get('first', None)
    last = flask.request.args.get('last', None)

    rsp = AppConfig.services.ratings.find_players(mid, first, last)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def get_details(mid):
    rsp = AppConfig.services.ratings.get_player_details(mid)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)
