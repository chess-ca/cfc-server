
import sqlalchemy as sa
from sqlalchemy.future import select
from .schema import t_event, t_crosstable, t_player
from codeboy4py.db.sqlalchemy import dataset

_max_rows = 500
_ta1_player = t_player.alias('ta1_player')
_ta2_player = t_player.alias('ta2_player')


class _DataSets:
    find_for_player_0 = dataset(
        (t_event, 'id name date_end rating_type'),
        (t_crosstable, 'score games_played rating_pre rating_perf rating_post rating_indicator')
    )
    find_for_orgarb_0 = dataset(
        (t_event, 'id name date_end province pairings n_rounds n_players organizer_id arbiter_id'),
        (_ta1_player.c.name_first + ' ' + _ta1_player.c.name_last).label('organizer_name'),
        (_ta2_player.c.name_first + ' ' + _ta2_player.c.name_last).label('arbiter_name')
    )


def find_for_player(
        dbcon: sa.engine.Connection,
        cfc_id: int,
        dataset: str = '0',
):
    select_cols = _DataSets.find_for_player_0 if dataset == '0' else []
    sql = (
        select(*select_cols)
        .select_from(t_crosstable.join(t_event))
        .where(t_crosstable.c.cfc_id == cfc_id)
        .order_by(t_event.c.date_end.desc())
        .limit(_max_rows)
    )
    with dbcon.begin():
        result = dbcon.execute(sql)
        events = [row._asdict() for row in result]
    return events


def find_for_orgarb(
        dbcon: sa.engine.Connection,
        cfc_id: int,
        dataset: str = '0',
):
    select_cols = _DataSets.find_for_orgarb_0 if dataset == '0' else []
    sql = (
        select(*select_cols)
        .select_from(
            t_event
            .join(_ta1_player, t_event.c.organizer_id == _ta1_player.c.cfc_id)
            .join(_ta2_player, t_event.c.arbiter_id == _ta2_player.c.cfc_id))
        .where(sa.or_(
            t_event.c.organizer_id == cfc_id,
            t_event.c.arbiter_id == cfc_id))
        .order_by(t_event.c.date_end.desc(), t_event.c.name.asc())
        .limit(_max_rows)
    )
    with dbcon.begin():
        result = dbcon.execute(sql)
        events = [row._asdict() for row in result]
    return events
