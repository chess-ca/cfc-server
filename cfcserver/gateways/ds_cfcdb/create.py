
import csv, typing

import sqlalchemy as sa
from . import schema


def create_tables(dbcon):
    with dbcon.begin():
        schema.sa_metadata.create_all(dbcon)


def create_indices(dbcon):
    with dbcon.begin():
        schema.create_indices(dbcon)


def metadata_insert(dbcon, metadata):
    sql = sa.insert(schema.t_metadata)
    sqldata = [dict(key=k, value=v) for k, v in metadata.items()]
    with dbcon.begin():
        r = dbcon.execute(sql, sqldata)
    return r.rowcount


def members_load_from_csv_file(dbcon, csv_f: typing.TextIO):
    n_loaded = 0
    sql = sa.insert(schema.t_player)
    sqldata = []
    data_csv = csv.DictReader(csv_f)
    for row in data_csv:
        sqldata.append(dict(
            cfc_id=int(row['cfc_id']),
            cfc_expiry=str(row['cfc_expiry']),
            cfc_type=str(row['cfc_type']),
            # FYI: 2022-08: CFC-Tools changed names from GoMembership to JustGo
            gomembership_id=str(row['justgo_id']),
            fide_id=int(row['fide_id']),
            name_first=str(row['name_first']),
            name_first_lc=str(row['name_first']).lower(),
            name_last=str(row['name_last']),
            name_last_lc=str(row['name_last']).lower(),
            birthdate=str(row['birthdate']),
            gender=str(row['gender']),
            email=str(row['email']),
            phone=str(row['phone']),
            addr_line1=str(row['addr_line1']),
            addr_line2=str(row['addr_line2']),
            addr_city=str(row['addr_city']),
            addr_province=str(row['addr_province']),
            addr_postalcode=str(row['addr_postalcode']),
            regular_rating=int(row['regular_rating']),
            regular_indicator=int(row['regular_indicator']),
            quick_rating=int(row['quick_rating']),
            quick_indicator=int(row['quick_indicator']),
            notes=str(row['notes']),
            last_update=str(row['last_update']),
        ))
        if len(sqldata) >= 1000:
            with dbcon.begin():
                dbcon.execute(sql, sqldata)
            n_loaded += len(sqldata)
            sqldata = []

    if len(sqldata) >= 1:
        with dbcon.begin():
            dbcon.execute(sql, sqldata)
        n_loaded += len(sqldata)
    return n_loaded


def events_load_from_csv(dbcon, csv_f: typing.TextIO):
    n_loaded = 0
    sql = sa.insert(schema.t_event)
    sqldata = []
    data_csv = csv.DictReader(csv_f)
    for row in data_csv:
        sqldata.append(dict(
            # CSV
            # id,name,date_end,province,arbiter_id,organizer_id,pairings,rating_type,n_players,n_rounds
            id=int(row['id']),
            name=str(row['name']),
            date_end=str(row['date_end']),
            province=str(row['province']),
            arbiter_id=int(row['arbiter_id']),
            organizer_id=int(row['organizer_id']),
            pairings=str(row['pairings']),
            rating_type=str(row['rating_type']),
            n_players=int(row['n_players']),
            n_rounds=int(row['n_rounds']),
            # SCHEMA
            # id name date_end province arbiter_id organizer_id
            # pairings rating_type n_players n_rounds
        ))
        if len(sqldata) >= 1000:
            with dbcon.begin():
                dbcon.execute(sql, sqldata)
            n_loaded += len(sqldata)
            sqldata = []

    if len(sqldata) >= 1:
        with dbcon.begin():
            dbcon.execute(sql, sqldata)
        n_loaded += len(sqldata)
    return n_loaded


def results_load_from_csv(dbcon, csv_f: typing.TextIO):
    n_loaded = 0
    sql = sa.insert(schema.t_crosstable)
    sqldata = []
    data_csv = csv.DictReader(csv_f)
    for row in data_csv:
        sqldata.append(dict(
            # CSV
            # event_id,place,cfc_id,province,games_played,score,results,rating_type,rating_pre,rating_perf,rating_post,rating_indicator
            event_id=int(row['event_id']),
            place=int(row['place']),
            cfc_id=int(row['cfc_id']),
            province=str(row['province']),
            games_played=int(row['games_played']),
            score=float(row['score']),
            results=str(row['results']).strip(' []'),
            rating_type=str(row['rating_type']),
            rating_pre=int(row['rating_pre']),
            rating_perf=int(row['rating_perf']),
            rating_post=int(row['rating_post']),
            rating_indicator=int(row['rating_indicator']),
            # SCHEMA
            # event_id place cfc_id province games_played score results
            # rating_type rating_pre rating_perf rating_post rating_indicator
        ))
        if len(sqldata) >= 1000:
            with dbcon.begin():
                dbcon.execute(sql, sqldata)
            n_loaded += len(sqldata)
            sqldata = []

    if len(sqldata) >= 1:
        with dbcon.begin():
            dbcon.execute(sql, sqldata)
        n_loaded += len(sqldata)
    return n_loaded
