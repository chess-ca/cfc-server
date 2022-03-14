
from typing import Optional, Union, Any
from codeboy4py.py.coercion import str_to_int, CoercionError
from cfcserver import AppConfig
import cfcserver.gateways.ds_cfcdb.player as gw_player
import cfcserver.gateways.ds_cfcdb.event as gw_event
import cfcserver.gateways.ds_cfcdb.metadata as gw_meta


def find(
    ids: Optional[str] = None,
    name_first: Optional[str] = None,
    name_last: Optional[str] = None,
    sort: Optional[str] = '',
):
    rsp: dict[str, Any] = {}
    with AppConfig.CFCDB.connect() as dbcon:
        rsp['updated'] = gw_meta.get_key(dbcon, 'updated_text')
        if ids is not None:
            ids = [str_to_int(i, if_bad=-1) for i in ids.split(',')]
            players = gw_player.find_by_ids(dbcon, ids, sort=sort)
        elif name_first is not None or name_last is not None:
            players = gw_player.find_by_names(dbcon, name_first, name_last)
        else:
            players = []
        rsp['players'] = players
    return rsp


def get_details(cfc_id: str) -> dict:
    cfc_id = str_to_int(str(cfc_id), if_bad=-1)
    rsp: dict[str, Any] = {}
    with AppConfig.CFCDB.connect() as dbcon:
        rsp['updated'] = gw_meta.get_key(dbcon, 'updated_text')
        # ids = [str_to_int(cfc_id, if_bad=-1)]
        plist = gw_player.find_by_ids(dbcon, [cfc_id])
        if len(plist) < 1:
            rsp['player'] = {'cfc_id': cfc_id, 'events': []}
            return rsp
        rsp['player'] = plist[0]
        rsp['player']['events'] = gw_event.find_for_player(dbcon, cfc_id)
        rsp['player']['orgarb'] = gw_event.find_for_orgarb(dbcon, cfc_id)
        roles = {'p': len(plist[0]) > 0, 'o': False, 'a': False}
        is_org, is_arb = False, False
        for e in rsp['player']['orgarb']:
            is_org = is_org or (e['organizer_id'] == cfc_id)
            is_arb = is_arb or (e['arbiter_id'] == cfc_id)
            if is_org and is_arb: break
        rsp['player']['is_organizer'] = is_org
        rsp['player']['is_arbiter'] = is_arb
    return rsp


def find_top_players(
    type: str = 'R',    # ratings type: R, RH, Q, QH
    topn: int = -1,     # number of top players
    rating_min: int = 0,
    rating_max: int = 9999,
    age_min: int = 0,
    age_max: int = 99,
    gender: str = '',
    province: str = '',
    last_played: str = '',
    cfc_expiry_min: str = '',
):
    with AppConfig.CFCDB.connect() as dbcon:
        rsp = {'updated': gw_meta.get_key(dbcon, 'updated_text')}
        rsp.update(**gw_player.find_top_players(
            dbcon, type=type, topn=topn,
            rating_min=rating_min, rating_max=rating_max,
            age_min=age_min, age_max=age_max,
            gender=gender, province=province,
            last_played=last_played, cfc_expiry_min=cfc_expiry_min,
        ))
    return rsp