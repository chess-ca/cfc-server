
import flask
import app
from ui_api.shared import api_response


def find():
    mid = flask.request.args.get('mid', None)
    first = flask.request.args.get('first', None)
    last = flask.request.args.get('last', None)

    rsp = app.services.ratings.find_players(mid, first, last)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def get_details(mid):
    rsp = app.services.ratings.get_player_details(mid)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)
