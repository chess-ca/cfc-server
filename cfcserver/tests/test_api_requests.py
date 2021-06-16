
import pathlib, sys, unittest
from urllib.request import urlopen
from urllib.parse import quote as url_quote

_hostname = 'http://127.0.0.1:5000'
_prefix = '/api/ratings'

root_path = pathlib.Path(__file__).resolve().parents[2]
# if str(root) not in sys.path:
#     sys.path.insert(0, str(root))

class TestAPIs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_player_find(self):
        url = f'{_hostname}{_prefix}/player/find?last=parakin'
        with urlopen(url, timeout=1) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertTrue(b'apicode' in body)
            self.assertTrue(b'Parakin' in body)

    def test_player(self):
        url = f'{_hostname}{_prefix}/player/101737'
        with urlopen(url, timeout=1) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertTrue(b'apicode' in body)
            self.assertTrue(b'Findlay, Ian' in body)

    def test_tournament(self):
        url = f'{_hostname}{_prefix}/tournament/202001035'
        with urlopen(url, timeout=1) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertTrue(b'apicode' in body)
            self.assertTrue(b'2020 Ottawa Winter U1600' in body)

    def test_tournament_find(self):
        url = f'{_hostname}{_prefix}/tournament/find?name='+url_quote('*hart house*')
        with urlopen(url, timeout=1) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertTrue(b'apicode' in body)
            self.assertTrue(b'Hart House Reading Week Crown' in body)

    def test_tournament_days(self):
        url = f'{_hostname}{_prefix}/tournament/days/60'
        with urlopen(url, timeout=1) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertTrue(b'apicode' in body)
            self.assertTrue(b'"tournaments":' in body)

    def test_tournament_year(self):
        url = f'{_hostname}{_prefix}/tournament/year/2020'
        with urlopen(url, timeout=1) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertTrue(b'apicode' in body)
            self.assertTrue(b'"tournaments":' in body)
