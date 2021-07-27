
import sqlalchemy as sa
from sqlalchemy.future import select
from sqlalchemy.sql import insert, update
from .schema import t_metadata


def get_key(dbcon: sa.engine.Connection, key: str, default=None):
    sql = select(t_metadata) \
        .where(t_metadata.c.key == key)
    with dbcon.begin():
        row = dbcon.execute(sql).fetchone()
    val = default if row is None else row.value
    return val


def set_key(dbcon: sa.engine.Connection, key: str, value: str):
    sql = update(t_metadata) \
        .where(t_metadata.c.key == key) \
        .values(value=value)
    with dbcon.begin():
        dbcsr = dbcon.execute(sql)
        if dbcsr.rowcount < 1:
            sql = insert(t_metadata) \
                .values(key=key, value=value)
            dbcon.execute(sql)
