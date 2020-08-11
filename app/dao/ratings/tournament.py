
import bnc4py.db.database as bnc_db
import app


def get_tid(db: bnc_db.Database, tid):
    sql = """
    SELECT t.*, p.first||' '||p.last AS org_name
        FROM tournament AS t LEFT JOIN player AS p ON t.org_m_id = p.m_id
        WHERE t.t_id = ?  
    """
    row = db.fetchone(sql, [tid])
    return None if not row \
        else db.row_to_dataclass(row, app.models.Tournament)


def get_for_player(db: bnc_db.Database, player):
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
        ce = db.row_to_dataclass(row, app.models.CrosstableEntry)
        player.tournaments.append(ce)


def get_crosstable_for_tournament(db: bnc_db.Database, tournament):
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
        ce = db.row_to_dataclass(row, app.models.CrosstableEntry)
        tournament.crosstable.append(ce)
