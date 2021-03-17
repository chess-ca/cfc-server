
import datetime
import codeboy4py.db.database as cb4py_db
import cfcserver.models as models


def get_tid(db: cb4py_db.GenericDatabase, tid):
    sql = """
    SELECT t.*, p.first||' '||p.last AS org_name
        FROM tournament AS t LEFT JOIN player AS p ON t.org_m_id = p.m_id
        WHERE t.t_id = ?  
    """
    row = db.fetchone(sql, [tid])
    return None if not row \
        else db.row_to_dataclass(row, models.Tournament)


def get_for_player(db: cb4py_db.GenericDatabase, player):
    sql = f"""
    SELECT t.*, ct.*
        FROM tournament AS t
            JOIN crosstable AS ct USING(t_id)
        WHERE ct.m_id = ?
        ORDER BY t.last_day DESC
    """
    player.tournaments = []
    rowset = db.fetchrows(sql, [player.m_id])
    for row in rowset:
        ce = db.row_to_dataclass(row, models.CrosstableEntry)
        player.tournaments.append(ce)


def get_crosstable_for_tournament(db: cb4py_db.GenericDatabase, tournament):
    sql = """
    SELECT t.*, ct.*, p.last||', '||p.first AS m_name
        FROM tournament AS t
            JOIN crosstable AS ct USING(t_id)
            JOIN player AS p ON p.m_id = ct.m_id
        WHERE ct.t_id = ?
        ORDER BY ct.place ASC
    """
    tournament.crosstable = []
    rowset = db.fetchrows(sql, [tournament.t_id])
    for row in rowset:
        ce = db.row_to_dataclass(row, models.CrosstableEntry)
        tournament.crosstable.append(ce)


def getall_name(db: cb4py_db.GenericDatabase, name):
    name = '%' + str(name).strip('* ').replace('*', '%') + '%'
    sql = """
    SELECT t.*, p.first||' '||p.last AS org_name
        FROM tournament AS t
            LEFT JOIN player AS p ON t.org_m_id = p.m_id
        WHERE t.name LIKE ? COLLATE NOCASE
        ORDER BY t.last_day DESC
        LIMIT 1000
    """
    for row in db.fetchrows(sql, [name]):
        yield db.row_to_dataclass(row, models.Tournament)


def getall_lastdays(db: cb4py_db.GenericDatabase, days):
    try: days = int(days)
    except ValueError: return   # zero tournaments if days is invalid
    date_from = (datetime.date.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    sql = """
    SELECT t.*, p.first||' '||p.last AS org_name
        FROM tournament AS t
            LEFT JOIN player AS p ON t.org_m_id = p.m_id
        WHERE t.last_day >= ?
        ORDER BY t.last_day DESC
        LIMIT 2000
    """
    for row in db.fetchrows(sql, [date_from]):
        yield db.row_to_dataclass(row, models.Tournament)


def getall_year(db: cb4py_db.GenericDatabase, year):
    try: year = int(year)
    except ValueError: return   # zero tournaments if days is invalid
    year_range = [f'{year}-00-00', f'{year}-99-99']
    sql = """
    SELECT t.*, p.first||' '||p.last AS org_name
        FROM tournament AS t
            LEFT JOIN player AS p ON t.org_m_id = p.m_id
        WHERE t.last_day >= ? AND t.last_day <= ?
        ORDER BY t.last_day DESC
        LIMIT 2000
    """
    for row in db.fetchrows(sql, year_range):
        yield db.row_to_dataclass(row, models.Tournament)
