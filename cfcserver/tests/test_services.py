
import pathlib, sys, io, unittest, importlib
import cfcserver
import cfcserver.services.player as s_player
import cfcserver.services.event as s_event

root_path = pathlib.Path(__file__).resolve().parents[2]


class TestServices(unittest.TestCase):
    log_file = io.StringIO()

    @classmethod
    def setUpClass(cls):
        print(f'Testing Services:')
        config = root_path / 'app_local/config/app.config.ini'
        cfcserver.initialize(str(config))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_cfcdb_player_find(self):
        rsp = s_player.find(ids='5555')
        self.assertIn('updated', rsp)
        self.assertIn('players', rsp)
        self.assertListEqual([], rsp['players'])
        rsp = s_player.find(ids='5555,6666')
        self.assertIn('updated', rsp)
        self.assertIn('players', rsp)
        self.assertListEqual([], rsp['players'])
        rsp = s_player.find(ids='106488')
        self.assertIsNotNone(rsp)
        self.assertIn('updated', rsp)
        self.assertIn('players', rsp)
        self.assertEqual(1, len(rsp['players']))
        self.assertIn('cfc_id', rsp['players'][0])
        rsp = s_player.find(ids='106488,108202,103201', sort='qr')
        self.assertIsNotNone(rsp)
        self.assertIn('updated', rsp)
        self.assertIn('players', rsp)
        self.assertEqual(3, len(rsp['players']))
        self.assertIn('cfc_id', rsp['players'][0])
        rsp = s_player.find(name_first=' DoN ', name_last='   pARAkIn ')
        self.assertEqual(len(rsp['players']), 1)
        rsp = s_player.find(name_first=' D* ', name_last='   pARA* ')
        self.assertGreater(len(rsp['players']), 1)

    def test_cfcdb_player_get_details(self):
        rsp = s_player.get_details('106488')
        self.assertIn('updated', rsp)
        self.assertIn('player', rsp)
        self.assertIn('events', rsp['player'])
        self.assertIn('orgarb', rsp['player'])

    def test_cfcdb_player_top(self):
        rsp = s_player.find_top_players(province='ON', age_min=50)
        self.assertIn('updated', rsp)
        self.assertIn('description', rsp)
        self.assertIn('en', rsp['description'])
        self.assertIn('fr', rsp['description'])
        self.assertIn('players', rsp)

    def test_cfcdb_event_find(self):
        # ---- name
        rsp = s_event.find(name='never-this-name-ever')
        self.assertIn('events', rsp)
        self.assertListEqual([], rsp['events'])
        rsp = s_event.find(name=' bu*y ')     # "Horse & Buggy Open"
        self.assertIn('events', rsp)
        event_ids = map(lambda e: e['id'], rsp['events'])
        self.assertIn(202110001, event_ids)
        # ---- year
        rsp = s_event.find(year=2021)
        year_is_2021 = map(lambda e: e['date_end'][:4]=='2021', rsp['events'])
        self.assertNotIn(False, year_is_2021)
        # ---- province
        rsp = s_event.find(year=2021, province='AB')
        prov_is_AB = map(lambda e: e['province'] == 'AB', rsp['events'])
        self.assertNotIn(False, prov_is_AB)
        # ---- days
        rsp = s_event.find(days=90)
        # Nothing to assert as there may be none as the test databases gets older

    def test_cfcdb_event_get_details(self):
        rsp = s_event.get_details(event_id='abc123')
        self.assertIn('event_id', rsp)
        self.assertEqual('abc123', rsp['event_id'])
        rsp = s_event.get_details(event_id='5555')
        self.assertIn('event', rsp)
        self.assertNotIn('name', rsp['event'])
        rsp = s_event.get_details(event_id=' 202110001  \t ')
        self.assertIn('event', rsp)
        self.assertIsNotNone(rsp['event'])
        self.assertIn('name', rsp['event'])
        self.assertEqual(rsp['event']['name'], 'Horse & Buggy Open')
        self.assertIn('organizer_name', rsp['event'])
        self.assertIn('arbiter_name', rsp['event'])
        self.assertEqual('Hal Bond', rsp['event']['arbiter_name'])
