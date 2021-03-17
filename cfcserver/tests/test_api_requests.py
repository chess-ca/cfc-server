
from urllib.request import urlopen
from urllib.parse import quote as url_quote

_hostname = 'http://127.0.0.1:5000'
_prefix = '/api/ratings'


def test_player_find():
    url = f'{_hostname}{_prefix}/player/find?last=parakin'
    with urlopen(url, timeout=1) as rsp:
        assert rsp.status == 200
        body = rsp.read()
        assert b'apicode' in body
        assert b'Parakin' in body

def test_player():
    url = f'{_hostname}{_prefix}/player/101737'
    with urlopen(url, timeout=1) as rsp:
        assert rsp.status == 200
        body = rsp.read()
        assert b'apicode' in body
        assert b'Findlay, Ian' in body

def test_tournament():
    url = f'{_hostname}{_prefix}/tournament/202001035'
    with urlopen(url, timeout=1) as rsp:
        assert rsp.status == 200
        body = rsp.read()
        assert b'apicode' in body
        assert b'2020 Ottawa Winter U1600' in body

def test_tournament_find():
    url = f'{_hostname}{_prefix}/tournament/find?name='+url_quote('*hart house*')
    with urlopen(url, timeout=1) as rsp:
        assert rsp.status == 200
        body = rsp.read()
        assert b'apicode' in body
        assert b'Hart House Reading Week Crown' in body

def test_tournament_days():
    url = f'{_hostname}{_prefix}/tournament/days/60'
    with urlopen(url, timeout=1) as rsp:
        assert rsp.status == 200
        body = rsp.read()
        assert b'apicode' in body
        assert b'"tournaments":' in body

def test_tournament_year():
    url = f'{_hostname}{_prefix}/tournament/year/2020'
    with urlopen(url, timeout=1) as rsp:
        assert rsp.status == 200
        body = rsp.read()
        assert b'apicode' in body
        assert b'"tournaments":' in body
