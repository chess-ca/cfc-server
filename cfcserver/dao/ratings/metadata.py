
import bnc4py.db.database as bnc_db

def get_key(db: bnc_db.GenericDatabase, key):
    sql = 'SELECT value FROM metadata WHERE key=?'
    row = db.fetchone(sql, [key])
    value = row['value'] if row else None
    return value
