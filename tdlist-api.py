#!/usr/bin/env python3.7
# REQUIRED: For CGI, chmod 711; a shebang; and Unix LF (not Windows CRLF)

import sqlite3, json, os, configparser, pathlib
import cgi, cgitb

# print('content-type: text/html')

config_fp = pathlib.Path(__file__).with_suffix('.config')
config_cp = configparser.ConfigParser()
config_cp.read(config_fp)
config = config_cp['tdlist-api']


def main():
    if config['tdlist_run_type'] == 'local':
        # request_players(cfc_id='106488')
        request_players(first='Dona*')
        # request_players(last='Para*')
    else:
        cgitb.enable(display=0, logdir=config['tdlist_log'])
        req = form = cgi.FieldStorage(encoding='utf-8')
        cfc_id = req['cfc_id'].value if 'cfc_id' in req else None
        first = req['first'].value if 'first' in req else None
        last = req['last'].value if 'last' in req else None
        request_players(cfc_id=cfc_id, first=first, last=last)


def request_players(cfc_id=None, last=None, first=None):
    where = []
    sqldata = []
    if cfc_id:
        where.append('cfc_id=?')
        sqldata.append(cfc_id)
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

    with Sqlite_Dbcon(config['tdlist_sqlite']) as dbcon:
        dbcsr = dbcon.cursor()
        # ---- Get the datetime of this database
        sql = 'SELECT value FROM metadata WHERE key=?'
        dbcsr.execute(sql, ['created'])
        row = dbcsr.fetchone()
        dbdate = row['value'] if row else None
        # ---- Get the player data
        sql = 'SELECT * FROM players WHERE ### ORDER BY last_lc'
        sql = sql.replace('###', ' AND '.join(where))
        # print(f'DEBUG: SQL: {sql}')
        # print(f'DEBUG: SQLDATA: {sqldata}')
        dbcsr = dbcon.cursor()
        pdata = []
        for player in dbcsr.execute(sql, sqldata):
            pdata.append(player['data'])
        # ---- Respond
        respond(0, players=pdata, dbdate=dbdate)
        # if len(pdata) == 0:
        #     respond_error(101, f'NOT FOUND: Zero players were found')
        # else:
        #     respond_players(pdata)


def respond(apicode, players=None, dbdate=None, errmsg=None):
    print('Content-Type: application/json')
    print('Cache-Control: public, max-age=60, must-revalidate')
    print('Access-Control-Allow-Origin: *')
    print('Status: 200')   # http status (transport layer) is not apicode (application layer)
    print()
    errmsg = errmsg.replace('"', '\\"') if errmsg else ''
    dbdate = dbdate or ''
    count = len(players) if players else 0
    pdata = ('\n' + (',\n'.join(players)) + '\n') if players else ''
    print(f'{{"apicode":{apicode}, "error":"{errmsg}", "count":{count}, "players":[{pdata}], "dbdate":"{dbdate}"}}')


class Sqlite_Dbcon:
    def __init__(self, sqlite_fpath):
        self.sqlite_fpath = sqlite_fpath
        if not os.path.exists(self.sqlite_fpath):
            raise Exception(f'ERROR: sqlite db not found: {self.sqlite_fpath}')
    def __enter__(self):
        self.dbcon = sqlite3.connect(self.sqlite_fpath)
        self.dbcon.row_factory = sqlite3.Row
        return self.dbcon
    def __exit__(self, type, value, traceback):
        self.dbcon.close()


main()
