
import flask
from cfcserver.ui.api.shared import api_response
from cfcserver.services import ratings as s_ratings


def find():
    mid = flask.request.args.get('mid', None)
    first = flask.request.args.get('first', None)
    last = flask.request.args.get('last', None)

    rsp = s_ratings.find_players(mid, first, last)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def get_details(mid):
    rsp = s_ratings.get_player_details(mid)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)
