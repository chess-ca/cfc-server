
import pathlib, io, unittest
import cfcserver
import cfcserver.gateways.ds_cfcdb.player as gw_player
import cfcserver.gateways.ds_cfcdb.event as gw_event
import cfcserver.gateways.ds_cfcdb.metadata as gw_meta

root_path = pathlib.Path(__file__).resolve().parents[2]


class TestGateway(unittest.TestCase):
    log_file = io.StringIO()
    dbcon = None

    @classmethod
    def setUpClass(cls):
        print(f'Testing Gateways:')
        config = root_path / 'app_local/config/app.config.ini'
        cfcserver.initialize(str(config))
        cls.dbcon = cfcserver.AppConfig.CFCDB.connect()

    @classmethod
    def tearDownClass(cls):
        if cls.dbcon: cls.dbcon.close()

    def test_cfcdb_metadata(self):
        val = gw_meta.get_key(self.dbcon, 'ziffle')
        self.assertIsNone(val)
        val = gw_meta.get_key(self.dbcon, 'updated_text')
        self.assertIsNotNone(val)
        self.assertTrue(str(val).startswith('202'))  # a year: 2022-...

    def test_cfcdb_player_find_by_ids(self):
        p = gw_player.find_by_ids(self.dbcon, ids=[5555])
        self.assertListEqual([], p)
        p = gw_player.find_by_ids(self.dbcon, ids=[106488,108202], sort='rr')
        self.assertIsNotNone(p)
        self.assertEqual(2, len(p))

    def test_cfcdb_player_find_by_names(self):
        run = lambda n1, n2: gw_player.find_by_names(self.dbcon, name_first=n1, name_last=n2)
        self.assertListEqual([], run('ziffle', 'zodnosky'))
        self.assertEqual(1, len(run('  DON ', '  PAraKIN ')))
        self.assertEqual(1, len(run('Don', 'parak*')))
        self.assertLessEqual(2, len(run('d*', 'par*')))

    def test_cfcdb_player_find_top_players(self):
        plist = gw_player.find_top_players(self.dbcon, topn=23)
        self.assertIsNotNone(plist)
        self.assertTrue('description' in plist)
        self.assertTrue('players' in plist)
        self.assertEqual(23, len(plist['players']))

    def test_cfcdb_event_find_for_id(self):
        event = gw_event.find_for_id(self.dbcon, event_id=5555)
        self.assertIsNone(event)
        event = gw_event.find_for_id(self.dbcon, event_id=202110001)
        self.assertIsNotNone(event)
        self.assertTrue('name' in event)
        self.assertEqual(event['name'], 'Horse & Buggy Open')
        self.assertTrue('organizer_name' in event)
        self.assertTrue('arbiter_name' in event)
        self.assertEqual('Hal Bond', event['arbiter_name'])

    def test_cfcdb_event_crosstable_for_id(self):
        xtable = gw_event.crosstable_for_id(self.dbcon, event_id=5555)
        self.assertEqual(0, len(xtable))
        xtable = gw_event.crosstable_for_id(self.dbcon, event_id=202110001)
        self.assertLess(10, len(xtable))
        self.assertTrue('name' in xtable[0])

    def test_cfcdb_event_find_for_player(self):
        elist = gw_event.find_for_player(self.dbcon, cfc_id=5555)
        self.assertListEqual([], elist)
        elist = gw_event.find_for_player(self.dbcon, cfc_id=106488)
        self.assertIsNotNone(elist)
        self.assertLess(0, len(elist))
        self.assertTrue('score' in elist[0])        # player's column
        self.assertTrue('date_end' in elist[0])     # event's column

    def test_cfcdb_event_find_for_orgarb(self):
        elist = gw_event.find_for_orgarb(self.dbcon, cfc_id=5555)
        self.assertListEqual([], elist)
        elist = gw_event.find_for_orgarb(self.dbcon, cfc_id=102713) #106488)
        self.assertIsNotNone(elist)
        self.assertLess(0, len(elist))
        self.assertTrue('n_players' in elist[0])        # event's column
        self.assertTrue('organizer_name' in elist[0])   # player's column
        self.assertTrue('arbiter_name' in elist[0])     # player's column

    def test_cfcdb_event_find_events(self):
        # ---- name
        elist = gw_event.find(self.dbcon, name='never-this-name-ever')
        self.assertListEqual([], elist)
        elist = gw_event.find(self.dbcon, name=' bu*y ')     # "Horse & Buggy Open"
        event_ids = map(lambda e: e['id'], elist)
        self.assertIn(202110001, event_ids)
        # ---- year
        elist = gw_event.find(self.dbcon, year=2021)
        year_is_2021 = map(lambda e: e['date_end'][:4]=='2021', elist)
        self.assertNotIn(False, year_is_2021)
        # ---- province
        elist = gw_event.find(self.dbcon, year=2021, province='AB')
        prov_is_AB = map(lambda e: e['province'] == 'AB', elist)
        self.assertNotIn(False, prov_is_AB)
        # ---- days
        elist = gw_event.find(self.dbcon, days=90)
        # Nothing to assert as there may no longer be any in the test database
