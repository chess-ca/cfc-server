
import flask, logging
import codeboy4py.py.pydantic as pd
from .shared import api_response
import cfcserver.services.player as s_player

_log = logging.getLogger('cfcserver')


class _API(pd.BaseModelPlus):
    type: str = 'R'     # ratings type: R, RH, Q, QH
    topn: int = -1      # number of top players
    rating_min: int = 0
    rating_max: int = 9999
    age_min: int = 0
    age_max: int = 99
    gender: str = ''
    province: str = ''
    last_played: str = ''
    cfc_expiry_min: str = ''


def find_top_players_v1():
    api_args = flask.request.args.to_dict()
    api_args, errs = _API.new(api_args)
    if errs:
        rsp = dict(apicode=9, errors=pd.simplify_errors(errs))
    else:
        api_args = api_args.dict()
        result = s_player.find_top_players(**api_args)
        rsp = dict(apicode=0, errors=[], **result)
    return api_response(rsp)
