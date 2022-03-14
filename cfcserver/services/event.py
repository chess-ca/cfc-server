
from typing import Any
from codeboy4py.py.coercion import str_to_int
from cfcserver import AppConfig
from cfcserver.gateways.ds_cfcdb import get_dbcon
import cfcserver.gateways.ds_cfcdb.metadata as gw_meta
import cfcserver.gateways.ds_cfcdb.event as gw_event


def find(
    name: str = '',
    province: str = '',
    year: int = -99,
    days: int = -99,
):
    rsp: dict[str, Any] = {}
    with get_dbcon() as dbcon:
        rsp['updated'] = gw_meta.get_key(dbcon, 'updated_text')
        rsp['events'] = gw_event.find(dbcon, name=name, province=province, year=year, days=days)
    return rsp


def get_details(event_id):
    rsp = {'event_id': str(event_id).strip()}
    with get_dbcon() as dbcon:
        rsp['updated'] = gw_meta.get_key(dbcon, 'updated_text')
        eid = str_to_int(str(event_id), if_bad=-1)
        if eid != -1:
            event = gw_event.find_for_id(dbcon, event_id=eid)
            rsp['event'] = event or {}
            if event:
                xtable = gw_event.crosstable_for_id(dbcon, eid)
                rsp['event']['crosstable'] = xtable or []
    return rsp
