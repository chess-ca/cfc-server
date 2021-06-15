
import flask
from cfcserver import AppConfig
from cfcserver.ui.api.shared import api_response


def get_details(tid):
    rsp = AppConfig.services.ratings.get_tournament_crosstable(tid)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def find():
    name = flask.request.args.get('name', None)
    rsp = AppConfig.services.ratings.find_tournaments(name)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def days(days):
    rsp = AppConfig.services.ratings.find_tournaments_days(days)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def year(year):
    rsp = AppConfig.services.ratings.find_tournaments_year(year)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)
