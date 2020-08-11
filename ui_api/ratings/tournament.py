
import flask as f
import app

_maxage = app.config.RATINGS_CACHE_MAXAGE


def get_details(tid):
    rsp = app.services.ratings.get_tournament_crosstable(tid)
    rsp = dict(apicode=0, error='', **rsp)

    ro = f.make_response(rsp)
    ro.headers['Cache-Control'] = f'public, max-age={_maxage}, must-revalidate'
    ro.headers['Access-Control-Allow-Origin'] = '*'
    return ro
