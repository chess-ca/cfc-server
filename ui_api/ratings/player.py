
import flask as f
import app

_maxage = app.config.RATINGS_CACHE_MAXAGE


def find():
    mid = f.request.args.get('mid', None)
    first = f.request.args.get('first', None)
    last = f.request.args.get('last', None)

    rsp = app.services.ratings.find_players(mid, first, last)
    rsp = dict(apicode=0, error='', **rsp)

    ro = f.make_response(rsp)
    ro.headers['Cache-Control'] = f'public, max-age={_maxage}, must-revalidate'
    ro.headers['Access-Control-Allow-Origin'] = '*'
    return ro


def get_details(mid):
    rsp = app.services.ratings.get_player_details(mid)
    rsp = dict(apicode=0, error='', **rsp)

    ro = f.make_response(rsp)
    ro.headers['Cache-Control'] = f'public, max-age={_maxage}, must-revalidate'
    ro.headers['Access-Control-Allow-Origin'] = '*'
    return ro
