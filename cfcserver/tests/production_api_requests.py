import json
import pathlib, sys, unittest, ssl
from urllib.request import urlopen
from urllib.parse import quote as url_quote

_hostname = 'https://server.chess.ca'
_prefix = '/api/ratings'

root_path = pathlib.Path(__file__).resolve().parents[2]
# if str(root) not in sys.path:
#     sys.path.insert(0, str(root))
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

class TestAPIs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(f'**** PRODUCTION **** Testing APIs:')

    @classmethod
    def tearDownClass(cls):
        pass

    # ---- Player's Details
    def test_v0_player(self):
        url = f'{_hostname}{_prefix}/player/101737'
        print(f'... API: v0: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'Findlay, Ian', body)

    def test_v1_player(self):
        url = f'{_hostname}/api/player/v1/106488'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('player', data)
            self.assertIn('events', data.get('player', {}))
            self.assertIn('orgarb', data.get('player', {}))

    # ---- Find Players
    def test_v0_player_find(self):
        url = f'{_hostname}{_prefix}/player/find?last=parakin'
        print(f'... API: v0: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'Parakin', body)

    def test_v1_player_find_ids(self):
        url = f'{_hostname}/api/player/v1/find?ids=106488'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('players', data)
        url = f'{_hostname}/api/player/v1/find?ids=106488,108202,103201&sort=rr'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('players', data)
            print('****', data)

    def test_v1_player_find_names(self):
        url = f'{_hostname}/api/player/v1/find?first={url_quote("d*")}&last={url_quote("para*")}'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('players', data)

    # ---- Top Players
    def test_v0_player_top(self):
        url = f'{_hostname}/api/cfcdb/player/v1/top'
        url += '?topn=50&type=R&province=ON&age_min=8&age_max=18'
        print(f'... API: v0: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'"description":', body)
            self.assertIn(b'"players":', body)

    def test_v1_player_top(self):
        url = f'{_hostname}/api/player/v1/top'
        url += '?topn=50&type=R&province=ON&age_min=8&age_max=18'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'"description":', body)
            self.assertIn(b'"players":', body)

    # ---- Event's Details
    def test_v0_tournament(self):
        url = f'{_hostname}{_prefix}/tournament/202001035'
        print(f'... API: v0: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'2020 Ottawa Winter U1600', body)

    def test_v1_event(self):
        url = f'{_hostname}/api/event/v1/202001035'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'2020 Ottawa Winter U1600', body)

    # ---- Find Events
    def test_v0_tournament_find(self):
        url = f'{_hostname}{_prefix}/tournament/find?name='+url_quote('*hart house*')
        print(f'... API: v0: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'Hart House Reading Week Crown', body)

    def test_v1_event_find(self):
        url = f'{_hostname}/api/event/v1/find?n='+url_quote('*hart house*')
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'Hart House Reading Week Crown', body)

    # ---- List Events - Days (DEPRECATING)
    def test_v0_tournament_days(self):
        url = f'{_hostname}{_prefix}/tournament/days/60'
        print(f'... API: v0: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'"tournaments":', body)

    # ---- List Events - Year (DEPRECATING)
    def test_v0_tournament_year(self):
        url = f'{_hostname}{_prefix}/tournament/year/2020'
        print(f'... API: v0: {url}')
        with urlopen(url, timeout=3, context=_ctx) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'"tournaments":', body)

    # ---- Top Organizers / Arbiters
    # def test_v1_orgarb_top(self):
    #     url = f'{_hostname}/api/orgarb/v1/top'
    #     print(f'... API: v1: {url}')
    #     with urlopen(url, timeout=3) as rsp:
    #         self.assertEqual(rsp.status, 200)
    #         body = rsp.read()
    #         self.assertIn(b'apicode', body)
    #         # self.assertIn(b'"tournaments":', body)
