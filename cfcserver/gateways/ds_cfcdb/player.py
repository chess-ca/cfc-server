
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.future import select
from sqlalchemy.sql import between
from codeboy4py.db.sqlalchemy import dataset
from .schema import t_player, t_event, t_crosstable

_max_rows = 500


class _DataSets:
    find_by_x_0 = dataset(
        (t_player, 'cfc_id cfc_expiry fide_id name_first name_last addr_city addr_province'
                   ' regular_rating regular_indicator quick_rating quick_indicator'),
    )


def find_by_ids(
        dbcon: sa.engine.Connection,
        ids: list[int],
        dataset: str = '0',
):
    select_cols = _DataSets.find_by_x_0 if dataset == '0' else []
    sql = (
        select(*select_cols)
        .where(t_player.c.cfc_id.in_(ids))
        .limit(_max_rows)
    )
    with dbcon.begin():
        result = dbcon.execute(sql)
        players = [row._asdict() for row in result]
    return players


def find_by_names(
        dbcon: sa.engine.Connection,
        name_first: str,
        name_last: str,
        dataset: str = '0',
):
    name_first = name_first.strip().lower()
    name_last = name_last.strip().lower()

    select_cols = _DataSets.find_by_x_0 if dataset == '0' else []
    sql = select(*select_cols)
    if name_first and name_first != '*':
        if '*' in name_first:
            name_first = name_first.replace('*', '%')
            sql = sql.where(t_player.c.name_first_lc.like(name_first))
        else:
            sql = sql.where(t_player.c.name_first_lc == name_first)
    if name_last and name_last != '*':
        if '*' in name_last:
            name_last = name_last.replace('*', '%')
            sql = sql.where(t_player.c.name_last_lc.like(name_last))
        else:
            sql = sql.where(t_player.c.name_last_lc == name_last)
    sql = sql.limit(_max_rows)
    with dbcon.begin():
        result = dbcon.execute(sql)
        players = [row._asdict() for row in result]
    return players


def find_top_players(
        dbcon: sa.engine.Connection,
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
        dataset: str = '0',
):
    now = datetime.now()
    extras_for_nth_place_ties = 50
    en, fr = [], []
    rating_type = type.upper()

    select_cols = _DataSets.find_by_x_0 if dataset == '0' else []
    sql = select(*select_cols)
    sql = sql.where(t_player.c.addr_province.not_in(['US', 'FO']))
    if topn > 0:
        en.append(f'Top {topn}')
        fr.append(f'Meilleurs {topn}')
        sql = sql.limit(topn + extras_for_nth_place_ties)
    else:
        en.append('All')
        fr.append('Tout')
    if rating_type == 'R':
        en.append('reqular ratings')
        fr.append('cotes régulières')
        sql = sql.order_by(t_player.c.regular_rating.desc(), t_player.c.name_last, t_player.c.name_first)
    elif rating_type == 'Q':
        en.append('quick ratings')
        fr.append('cotes rapides')
        sql = sql.order_by(t_player.c.quick_rating.desc(), t_player.c.name_last, t_player.c.name_first)
    if rating_min > 0 or rating_max < 9999:
        sql = sql.where(between(
            t_player.c.quick_rating if rating_type == 'Q' else t_player.c.regular_rating,
            max(1, rating_min),     # exclude ratings==0: player does not have a rating
            rating_max))
        en.append('rating{}{}'.format(
            f' {rating_min}' if rating_min > 0 else '',
            f' to {rating_max}' if rating_max < 9999 else '',
        ))
        fr.append('cote{}{}'.format(
            f' {rating_min}' if rating_min > 0 else '',
            f' à {rating_max}' if rating_max < 9999 else '',
        ))
    if age_min > 0 or age_max < 99:
        birth_max = '2090-99-99' if age_min <=0 \
            else f'{now.year - 1 - age_min}-99-99'
        # Must exclude fake birthdates 1901-01-01 to 1905-01-01
        birth_min = '1905-01-02' if age_max >= 99 \
            else f'{now.year - 1 - age_max}-00-00'
        sql = sql.where(between(t_player.c.birthdate, birth_min, birth_max))
        en.append('age{}{}'.format(
            f' {age_min}' if age_min > 0 else '',
            f' to {age_max}' if age_max < 99 and age_max != age_min else '',
        ))
        fr.append('{}{}ans'.format(
            f'{age_min} ' if age_min > 0 else '',
            f'à {age_max} ' if age_max < 99 and age_max != age_min else '',
        ))
    if gender:
        en.append(f'gender {gender.upper()}')
        fr.append(f'genre {gender.upper()}')
        sql = sql.where(t_player.c.gender == gender.upper())
    if province:
        en.append(f'province {province}')
        fr.append(f'province {province}')
        sql = sql.where(t_player.c.addr_province == province.upper())
    if cfc_expiry_min:
        en.append(f'CFC expiry on/after {cfc_expiry_min}')
        fr.append(f'FCE expiration le/après {cfc_expiry_min}')
        sql = sql.where(t_player.c.cfc_expiry >= cfc_expiry_min)
    if last_played:
        en.append(f'last played on/after {last_played}')
        fr.append(f'joué pour la dernière fois le/après {last_played}')
        sq_last_played = select(t_crosstable.c.cfc_id) \
            .select_from(t_crosstable.join(t_event, t_crosstable.c.event_id == t_event.c.id)) \
            .where(t_event.c.date_end >= last_played)
        sql = sql.where(t_player.c.cfc_id.in_(sq_last_played))
    sql = sql.limit(_max_rows)

    description = {'en': ', '.join(en), 'fr': ', '.join(fr)}
    players = []
    with dbcon.begin():
        # Must exclude extra players fetched if they have not tied for nth place
        prev_pos, prev_rating = -1, -1
        r_nth = 0
        result = dbcon.execute(sql)
        for n, row in enumerate(result):
            player = row._asdict()
            players_rating = player['quick_rating'] if rating_type == 'Q' \
                else player['regular_rating']
            if players_rating == prev_rating:
                player['pos'] = prev_pos
            else:
                player['pos'] = n + 1
                prev_pos, prev_rating = n + 1, players_rating

            if topn <= 0 or n < topn:
                # Player is in top n: include
                players.append(player)
                if n == topn - 1:
                    r_nth = players_rating
            elif players_rating == r_nth:
                # Player is tied for nth place: include
                players.append(player)
            else:
                # Player is NOT tied for nth place: exclude
                break   # since remaining players will also be != r_nth

    return dict(description=description, players=players)
