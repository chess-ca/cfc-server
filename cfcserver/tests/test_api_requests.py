import json
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
        print('Testing APIs:')

    @classmethod
    def tearDownClass(cls):
        pass

    # ---- Player's Details
    def test_v1_player(self):
        url = f'{_hostname}/api/player/v1/106488'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('player', data)
            self.assertIn('events', data.get('player', {}))
            self.assertIn('orgarb', data.get('player', {}))

    # ---- Find Players
    def test_v1_player_find_ids(self):
        url = f'{_hostname}/api/player/v1/find?ids=106488'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('players', data)
        url = f'{_hostname}/api/player/v1/find?ids=106488,108202,103201&sort=rr'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('players', data)

    def test_v1_player_find_names(self):
        url = f'{_hostname}/api/player/v1/find?first={url_quote("d*")}&last={url_quote("para*")}'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            data = json.loads(rsp.read())
            self.assertIn('updated', data)
            self.assertIn('players', data)

    # ---- Top Players
    def test_v1_player_top(self):
        url = f'{_hostname}/api/player/v1/top'
        url += '?topn=50&type=R&province=ON&age_min=8&age_max=18'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'"description":', body)
            self.assertIn(b'"players":', body)

    # ---- Event's Details
    def test_v1_event(self):
        url = f'{_hostname}/api/event/v1/202001035'
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'2020 Ottawa Winter U1600', body)

    # ---- Find Events
    def test_v1_event_find(self):
        url = f'{_hostname}/api/event/v1/find?n='+url_quote('Hart House')
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'Hart House Reading Week Crown', body)
        url = f'{_hostname}/api/event/v1/find?n='+url_quote('*Hart House   * ')
        print(f'... API: v1: {url}')
        with urlopen(url, timeout=3) as rsp:
            self.assertEqual(rsp.status, 200)
            body = rsp.read()
            self.assertIn(b'apicode', body)
            self.assertIn(b'Hart House Reading Week Crown', body)

    # ---- Top Organizers / Arbiters
    # def test_v1_orgarb_top(self):
    #     url = f'{_hostname}/api/orgarb/v1/top'
    #     print(f'... API: v1: {url}')
    #     with urlopen(url, timeout=3) as rsp:
    #         self.assertEqual(rsp.status, 200)
    #         body = rsp.read()
    #         self.assertIn(b'apicode', body)
    #         # self.assertIn(b'"tournaments":', body)
