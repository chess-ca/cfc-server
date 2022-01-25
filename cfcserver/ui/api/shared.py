
import flask
from cfcserver import AppConfig

def api_response(data):
    if isinstance(data, dict):
        if 'apicode' not in data:
            data['apicode'] = 0
        if 'error' not in data:
            data['error'] = ''

    _maxage = AppConfig.RATINGS_CACHE_MAXAGE
    ro = flask.make_response(data)
    ro.access_control_allow_origin = '*'
    ro.headers.add('Cache-Control', f'public, max-age={_maxage}, must-revalidate')
    ro.headers.add('Server', 'cfc-server')
    return ro


def csv_response(data: list[dict], filename=None):
    import csv, io
    csv_text = io.StringIO()
    col_names = ['empty'] if len(data) == 0 else data[0].keys()
    csv = csv.DictWriter(csv_text, fieldnames=col_names)
    csv.writeheader()
    csv.writerows(data)

    _maxage = AppConfig.RATINGS_CACHE_MAXAGE
    ro = flask.make_response(csv_text.getvalue())
    ro.mimetype = 'text/csv'
    filename = filename or 'cfc.data.csv'
    ro.headers.add('Content-Disposition', f'attachment; filename="{filename}"')
    ro.access_control_allow_origin = '*'
    ro.headers.add('Cache-Control', f'public, max-age={_maxage}, must-revalidate')
    ro.headers.add('Server', 'cfc-server')
    return ro
