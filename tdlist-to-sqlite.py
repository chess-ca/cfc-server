import types, os, sqlite3
from datetime import datetime

# tdlist_in = r'C:\_Google-Drive\Chess\Org - Tournaments\2020 Great Canadian Ratings Race\2020-07-01.CFC.tdlist.txt'
tdlist_in = r'C:\_TEMP\_TEST_tdlist\tdlist.txt'
rows_max = 999999999
p_attrs = ['cfc_id','last','first','city','expiry','rating','rating_high','active','active_high','fide_id']

def main():
    tdlist_sqlite(tdlist_in)
    # tdlist_clean(tdlist_in)


def tdlist_sqlite(tdlist_in):
    sqlite_fpath = f'{tdlist_in}.sqlite'
    with Sqlite_Dbcon(sqlite_fpath) as dbcon:
        for n, p in get_player(tdlist_in):
            vals = []
            for a in p_attrs:
                val = getattr(p, a, '')
                val = val if val.isdigit() else f'"{val}"'
                vals.append(f'"{a}":{val}')
            json = '{' + ', '.join(vals) + '}'
            dbcon.execute('INSERT INTO players (cfc_id, last_lc, first_lc, data) VALUES (?,?,?,?)',
                [p.cfc_id, p.last.lower(), p.first.lower(), json]
            )
            if n % 250 == 0:
                dbcon.commit()
        dbcon.commit()


def tdlist_clean(fpath_in):
    print(','.join([f'"{c}"' for c in p_attrs]))
    for n, p in get_player(tdlist_in):
        pvals = [f'"{getattr(p, a, "")}"' for a in p_attrs]
        print(','.join(pvals))


class Sqlite_Dbcon:
    def __init__(self, sqlite_fpath):
        self.sqlite_fpath = sqlite_fpath
    def __enter__(self):
        if os.path.exists(self.sqlite_fpath):
            os.remove(self.sqlite_fpath)
        now_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        self.dbcon = sqlite3.connect(self.sqlite_fpath)
        self.dbcon.execute('CREATE TABLE metadata (key text, value text)')
        self.dbcon.execute('INSERT INTO metadata (key, value) VALUES (?,?)', ['created', now_utc])
        self.dbcon.execute('CREATE TABLE players (cfc_id text, last_lc text, first_lc text, data text)')
        self.dbcon.execute('CREATE INDEX ix_cfc_id ON players (cfc_id)')
        self.dbcon.execute('CREATE INDEX ix_name ON players (last_lc, first_lc)')
        self.dbcon.commit()
        return self.dbcon
    def __exit__(self, type, value, traceback):
        self.dbcon.close()


def get_player(fpath_in, skip_row1=True):
    with open(fpath_in, 'r') as f:
        for n, line in enumerate(f):
            if n == 0 and skip_row1:
                continue
            elif n >= rows_max:
                return
            else:
                player = parseLine(line)
                yield n, player


def parseLine(line):
    # "CFC#","Expiry","Last","First","Prov","City","Rating","High","Active Rtg","Active High","FIDE Number","FIDE Rating"
    # tdlist file is malformed CSV so must scan it instead
    player = types.SimpleNamespace()
    i1,i2 = 0, line.find(',', 0)            # cfc id
    player.cfc_id = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find(',', i2+1)       # expiry
    dmy = (line[i1:i2].strip('" ')+'//').split('/')
    player.expiry = 'LIFE' if dmy[2] == '2099' \
        else '--' if dmy[2] <= '1960' \
        else f'{dmy[2]}-{dmy[1]}-{dmy[0]}'
    i1,i2 = i2+1, line.find(',', i2+1)       # last name
    player.last = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find(',', i2+1)       # first name
    player.first = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find(',', i2+1)       # province
    prov = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find('",', i2+1)      # city (may contain ','; always ends with '",'
    city = line[i1:i2].strip('" ') or '?'
    player.city = f'{city}, {prov}'.strip(', ')
    i1,i2 = i2+2, line.find(',', i2+2)       # rating
    player.rating = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find(',', i2+1)       # rating high
    player.rating_high = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find(',', i2+1)       # active
    player.active = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find(',', i2+1)       # active high
    player.active_high = line[i1:i2].strip('" ')
    i1,i2 = i2+1, line.find(',', i2+1)       # fide
    player.fide_id = line[i1:i2].strip('" ')
    return player

main()
