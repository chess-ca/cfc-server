
import flask
import app

def api_response(data):
    _maxage = app.config.RATINGS_CACHE_MAXAGE
    ro = flask.make_response(data)
    ro.headers['Cache-Control'] = f'public, max-age={_maxage}, must-revalidate'
    ro.headers['Access-Control-Allow-Origin'] = '*'
    ro.headers['server'] = 'cfc-server'
    return ro
