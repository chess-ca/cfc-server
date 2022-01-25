
import pathlib, sys, io, unittest, importlib
import cfcserver
import cfcserver.services.player as s_player

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
        rsp = s_player.find(ids='5555,6666')
        self.assertTrue('updated' in rsp)
        self.assertTrue('players' in rsp)
        self.assertListEqual([], rsp['players'])
        rsp = s_player.find(ids='106488,108202,103201')
        self.assertIsNotNone(rsp)
        self.assertTrue('updated' in rsp)
        self.assertTrue('players' in rsp)
        self.assertEqual(3, len(rsp['players']))
        self.assertTrue('cfc_id' in rsp['players'][0])
        rsp = s_player.find(name_first=' DoN ', name_last='   pARAkIn ')
        self.assertEqual(len(rsp['players']), 1)
        rsp = s_player.find(name_first=' D* ', name_last='   pARA* ')
        self.assertGreater(len(rsp['players']), 1)

    def test_cfcdb_player_get_details(self):
        rsp = s_player.get_details('106488')
        self.assertTrue('updated' in rsp)
        self.assertTrue('player' in rsp)
        self.assertTrue('events' in rsp['player'])
        self.assertTrue('orgarb' in rsp['player'])

    def test_cfcdb_player_top(self):
        rsp = s_player.find_top_players(province='ON', age_min=50)
        self.assertTrue('updated' in rsp)
        self.assertTrue('description' in rsp)
        self.assertTrue('en' in rsp['description'])
        self.assertTrue('fr' in rsp['description'])
        self.assertTrue('players' in rsp)
