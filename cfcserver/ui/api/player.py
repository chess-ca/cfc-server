
import flask, logging
from typing import Optional
import codeboy4py.py.pydantic as pd
from .shared import api_response, csv_response
import cfcserver.services.player as s_player

_log = logging.getLogger('cfcserver')


def find_v1():
    class _API(pd.BaseModelPlus):
        ids: Optional[str] = None
        first: Optional[str] = None
        last: Optional[str] = None
        sort: Optional[str] = ''
        csv: Optional[str] = None

    args, errs = _API.from_dict(flask.request.args.to_dict())
    if errs:
        rsp = dict(apicode=9, error=pd.simplify_errors(errs), players=[])
    else:
        rsp = s_player.find(ids=args.ids, name_first=args.first,
            name_last=args.last, sort=args.sort)
    rsp.setdefault('apicode', 0)
    rsp.setdefault('error', '')

    if args.csv is None:
        return api_response(rsp)
    else:
        updated = str(rsp['updated']).split(None, 1)[0]
        filename = f'cfc.member-data.{updated}.csv'
        return csv_response(rsp['players'], filename=filename)


def get_details_v1(cfc_id):
    rsp = s_player.get_details(cfc_id)
    return api_response(rsp)


def find_top_players_v1():
    class _API(pd.BaseModelPlus):
        type: str = 'R'     # ratings type: R, RH, Q, QH
        topn: int = 50      # number of top players
        rating_min: int = 0
        rating_max: int = 9999
        age_min: int = 0
        age_max: int = 99
        gender: str = ''
        province: str = ''
        last_played: str = ''
        cfc_expiry_min: str = ''

    api_args = flask.request.args.to_dict()
    api_args, errs = _API.from_dict(api_args)
    if errs:
        rsp = dict(apicode=9, errors=pd.simplify_errors(errs))
    else:
        api_args.topn = max(10, min(500, api_args.topn))
        api_args = api_args.dict()
        result = s_player.find_top_players(**api_args)
        rsp = dict(apicode=0, errors=[], **result)
    return api_response(rsp)
