
import csv, datetime

_tables = (
    ('metadata', (
        'key text', 'value text',
    )),
    ('player', (
        'm_id number', 'fide_id number', 'expiry text',
        'first text', 'last text', 'first_lc text', 'last_lc text',
        'city text', 'prov text',
        'sex text', 'birthdate text',
        'rating number', 'rating_hi number',
        'quick number', 'quick_hi number',
    )),
    ('tournament', (
        't_id number', 'name text', 'last_day text', 'prov text',
        'rounds number', 'pairings text', 'type text', 'org_m_id number',
    )),
    ('crosstable', (
        't_id number', 'place number', 'm_id number',
        'results text', 'score number', 'games_played number',
        'rating_pre number', 'rating_perf number', 'rating_post number',
        'rating_hi number',
    )),
)


def create_tables(db):
    for table_name, col_list in _tables:
        sql = 'CREATE TABLE "{}" ({})'.format(
            table_name, ', '.join(col_list))
        db.execute(sql)
    db.commit()

    sql = 'INSERT INTO metadata ("key", "value") VALUES (?, ?)'
    sqldata = [
        ('created', datetime.datetime.now().isoformat()),
        ('schema', '1.0'),
    ]
    db.executemany(sql, sqldata)
    db.commit()


def load_members_from_csv(db, csv_fpath):
    n_loaded = 0
    with open(csv_fpath, 'r') as csv_f:
        data_csv = csv.DictReader(csv_f)
        for row in data_csv:
            sqldata = dict(
                m_id=int(row['cfc_id']),
                fide_id=int(row['fide_id']),
                expiry=str(row['cfc_expiry']),
                first=str(row['name_first']),
                last=str(row['name_last']),
                first_lc=str(row['name_first']).lower(),
                last_lc=str(row['name_last']).lower(),
                city=str(row['addr_city']),
                prov=str(row['addr_province']),
                sex=str(row['gender']),
                birthdate=str(row['birthdate']),
                rating=int(row['regular_rating']),
                rating_hi=int(row['regular_indicator']),
                quick=int(row['quick_rating']),
                quick_hi=int(row['quick_indicator']),
            )
            keys = sqldata.keys()
            sql = 'INSERT INTO "player" ({}) VALUES ({})'.format(
                ','.join(keys), ','.join(['?' for k in keys]))
            db.execute(sql, [sqldata[k] for k in keys])
            n_loaded += 1
            if n_loaded % 1000 == 0:
                db.commit()
        db.commit()
    return n_loaded


def load_events_from_csv(db, csv_fpath):
    n_loaded = 0
    with open(csv_fpath, 'r') as csv_f:
        data_csv = csv.DictReader(csv_f)
        for row in data_csv:
            sqldata = dict(
                t_id=int(row['id']),
                name=str(row['name']),
                last_day=str(row['date_end']),
                prov=str(row['province']),
                rounds=int(row['n_rounds']),
                pairings=str(row['pairings']),
                type=str(row['rating_type']),
                org_m_id=str(row['organizer_id']),
            )
            keys = sqldata.keys()
            sql = 'INSERT INTO "tournament" ({}) VALUES ({})'.format(
                ','.join(keys), ','.join(['?' for k in keys]))
            db.execute(sql, [sqldata[k] for k in keys])
            n_loaded += 1
            if n_loaded % 1000 == 0:
                db.commit()
        db.commit()
    return n_loaded


def load_results_from_csv(db, csv_fpath):
    n_loaded = 0
    with open(csv_fpath, 'r') as csv_f:
        data_csv = csv.DictReader(csv_f)
        for row in data_csv:
            sqldata = dict(
                t_id=int(row['event_id']),
                place=int(row['place']),
                m_id=int(row['cfc_id']),
                results=str(row['results']).strip(' []'),
                score=float(row['score']),
                games_played=int(row['games_played']),
                rating_pre=int(row['rating_pre']),
                rating_perf=int(row['rating_perf']),
                rating_post=int(row['rating_post']),
                rating_hi=int(row['rating_indicator']),
            )
            keys = sqldata.keys()
            sql = 'INSERT INTO "crosstable" ({}) VALUES ({})'.format(
                ','.join(keys), ','.join(['?' for k in keys]))
            db.execute(sql, [sqldata[k] for k in keys])
            n_loaded += 1
            if n_loaded % 1000 == 0:
                db.commit()
        db.commit()
    return n_loaded


def insert_metadata(db, metadata):
    sqldata = [(key, value) for key, value in metadata.items()]
    sql = 'INSERT INTO "metadata" (key, value) VALUES (?, ?)'
    db.executemany(sql, sqldata)
    db.commit()
    return db.rowcount()
