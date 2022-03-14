
import datetime
import sqlalchemy as sa
from sqlalchemy.future import select
from .schema import t_event, t_crosstable, t_player
from codeboy4py.db.sqlalchemy import column_set

_max_rows = 1000
_ta1_player = t_player.alias('ta1_player')
_ta2_player = t_player.alias('ta2_player')


class _ColumnSets:
    find_0 = column_set(
        (t_event, 'id name date_end province pairings n_rounds n_players rating_type organizer_id arbiter_id'),
        (_ta1_player.c.name_first + ' ' + _ta1_player.c.name_last).label('organizer_name'),
        (_ta2_player.c.name_first + ' ' + _ta2_player.c.name_last).label('arbiter_name')
    )
    crosstable_for_id_0 = column_set(
        (t_crosstable, 'place cfc_id games_played score results rating_type rating_pre rating_perf rating_post rating_indicator'),
        (t_player.c.name_last + ', ' + t_player.c.name_first).label('name'),
    )
    find_for_player_0 = column_set(
        (t_event, 'id name date_end rating_type'),
        (t_crosstable, 'score games_played rating_pre rating_perf rating_post rating_indicator')
    )


def find(
        dbcon: sa.engine.Connection,
        name: str = '',
        province: str = '',
        year: int = -99,
        days: int = -99,
        dataset: str = '0',
):
    select_cols = _ColumnSets.find_0 if dataset == '0' else []
    sql = (
        select(*select_cols)
        .select_from(
            t_event
            .outerjoin(_ta1_player, t_event.c.organizer_id == _ta1_player.c.cfc_id)
            .outerjoin(_ta2_player, t_event.c.arbiter_id == _ta2_player.c.cfc_id)))
    if name:
        pattern = '%' + str(name).strip('* ').replace('*', '%') + '%'
        sql = sql.where(t_event.c.name.ilike(pattern))
    if province and province != '*':
        sql = sql.where(t_event.c.province == province)
    if days > 0:
        date_from = (datetime.date.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
        sql = sql.where(t_event.c.date_end >= date_from)
    elif year > 0:
        sql = sql.where(t_event.c.date_end > f'{year}-00-00')
        sql = sql.where(t_event.c.date_end < f'{year}-99-99')
    sql = sql.order_by(t_event.c.date_end.desc(), t_event.c.name.asc())
    sql = sql.limit(_max_rows)
    with dbcon.begin():
        result = dbcon.execute(sql)
        events = [row._asdict() for row in result]
    return events


def find_for_id(
        dbcon: sa.engine.Connection,
        event_id: int,
        dataset: str = '0',
):
    select_cols = _ColumnSets.find_0 if dataset == '0' else []
    sql = (
        select(*select_cols)
        .select_from(
            t_event
            .outerjoin(_ta1_player, t_event.c.organizer_id == _ta1_player.c.cfc_id)
            .outerjoin(_ta2_player, t_event.c.arbiter_id == _ta2_player.c.cfc_id))
        .where(t_event.c.id == event_id)
    )
    with dbcon.begin():
        result = dbcon.execute(sql)
        row = result.fetchone()
    return row._asdict() if row else None


def crosstable_for_id(
        dbcon: sa.engine.Connection,
        event_id: int,
        dataset: str = '0',
):
    select_cols = _ColumnSets.crosstable_for_id_0 if dataset == '0' else []
    sql = (
        select(*select_cols)
        .select_from(t_crosstable.join(t_player))
        .where(t_crosstable.c.event_id == event_id)
        .order_by(t_crosstable.c.place)
        .limit(_max_rows)
    )
    with dbcon.begin():
        result = dbcon.execute(sql)
        xtable = [row._asdict() for row in result]
    return xtable


def find_for_player(
        dbcon: sa.engine.Connection,
        cfc_id: int,
        dataset: str = '0',
):
    select_cols = _ColumnSets.find_for_player_0 if dataset == '0' else []
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
    select_cols = _ColumnSets.find_0 if dataset == '0' else []
    sql = (
        select(*select_cols)
        .select_from(
            t_event
            .outerjoin(_ta1_player, t_event.c.organizer_id == _ta1_player.c.cfc_id)
            .outerjoin(_ta2_player, t_event.c.arbiter_id == _ta2_player.c.cfc_id))
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
