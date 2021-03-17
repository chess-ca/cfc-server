
import codeboy4py.db.database as cb4py_db
import cfcserver.models as models


def get_mid(db: cb4py_db.GenericDatabase, mid):
    sql = 'SELECT * FROM player WHERE m_id=?'
    row = db.fetchone(sql, [mid])
    return None if not row \
        else db.row_to_dataclass(row, models.Player)


def getall_name(db: cb4py_db.GenericDatabase, first=None, last=None):
    where = []
    sqldata = []

    if last:
        if '*' not in last:
            where.append('last_lc=?')
        else:
            where.append('last_lc LIKE ?')
            last = last.replace('*', '%')
        sqldata.append(last.lower())

    if first:
        if '*' not in first:
            where.append('first_lc=?')
        else:
            where.append('first_lc LIKE ?')
            first = first.replace('*', '%')
        sqldata.append(first.lower())

    sql = 'SELECT * FROM player WHERE ### ORDER BY last_lc LIMIT 1000'
    sql = sql.replace('###', ' AND '.join(where))
    rowset = db.fetchrows(sql, sqldata)
    for row in rowset:
        yield db.row_to_dataclass(row, models.Player)
