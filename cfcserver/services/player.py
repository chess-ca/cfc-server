
from cfcserver import AppConfig


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
    import cfcserver.gateways.ds_cfcdb.player as gw_player
    import cfcserver.gateways.ds_cfcdb.metadata as gw_meta
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