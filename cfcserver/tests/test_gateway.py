
import pathlib, sys, io, unittest, importlib
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
        p = gw_player.find_by_ids(self.dbcon, ids=[106488,108202])
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
