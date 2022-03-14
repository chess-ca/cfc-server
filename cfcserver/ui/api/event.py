
import flask
import codeboy4py.py.pydantic as pd
from .shared import api_response
from cfcserver.services import event as s_event


def find_v1():
    class _API(pd.BaseModelPlus):
        n: str = ''         # name pattern (with "*" wildcard chars)
        p: str = ''         # province (2 letter code or "*" for all)
        y: int = -99        # year (events in year y)
        d: int = -99        # days (events in the last d days)

    args, errs = _API.from_dict(flask.request.args.to_dict())
    if errs:
        rsp = dict(apicode=9, error=pd.simplify_errors(errs), events=[])
    else:
        rsp = s_event.find(name=args.n, province=args.p, year=args.y, days=args.d)
        rsp.setdefault('apicode', 0)
        rsp.setdefault('error', '')
        print('okay:', args.n, 'rsp:', rsp)
    return api_response(rsp)


def get_details_v1(event_id):
    rsp = s_event.get_details(event_id)
    return api_response(rsp)
