
import flask
from cfcserver.ui.api.shared import api_response
from cfcserver.services import ratings as s_ratings


def get_details(tid):
    rsp = s_ratings.get_tournament_crosstable(tid)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def find():
    name = flask.request.args.get('name', None)
    rsp = s_ratings.find_tournaments(name)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def days(days):
    rsp = s_ratings.find_tournaments_days(days)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)


def year(year):
    rsp = s_ratings.find_tournaments_year(year)
    rsp = dict(apicode=0, error='', **rsp)
    return api_response(rsp)
