
import codeboy4py.db.database as cb4py_db


def get_key(db: cb4py_db.GenericDatabase, key):
    sql = 'SELECT value FROM metadata WHERE key=?'
    row = db.fetchone(sql, [key])
    value = row['value'] if row else None
    return value
