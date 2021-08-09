
import flask
from cfcserver import AppConfig

def api_response(data):
    _maxage = AppConfig.RATINGS_CACHE_MAXAGE
    ro = flask.make_response(data)
    ro.access_control_allow_origin = '*'
    ro.headers.add('Cache-Control', f'public, max-age={_maxage}, must-revalidate')
    ro.headers.add('Server', 'cfc-server')
    return ro
