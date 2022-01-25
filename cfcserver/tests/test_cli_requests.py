
import pathlib, sys, io, unittest, logging, importlib
from urllib.request import urlopen
from urllib.parse import quote as url_quote

_hostname = 'http://127.0.0.1:5000'
_prefix = '/api/ratings'

root_path = pathlib.Path(__file__).resolve().parents[2]
# if str(root) not in sys.path:
#     sys.path.insert(0, str(root))

class TestAPIs(unittest.TestCase):
    log_file = io.StringIO()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # def test_cfcdb_create(self):
    #     with self.assertLogs('cfcserver') as ctx:
    #         sys.argv = ['--local', '--dev', '--cli', 'cfcdb', '--job', str(root_path / 'app_local/jobs/test.cfcdb')]
    #         import main     # importing will invoke the CLI
    #         log_txt = '\n'.join(ctx.output)
    #         self.assertTrue('JOB ENDED:' in log_txt)

    def test_cfcdb_create(self):
        sys.argv = ['--local', '--dev', '--cli', 'cfcdb', '--job', str(root_path / 'app_local/jobs/test.cfcdb')]
        if 'main' not in sys.modules:
            import main     # importing will invoke the CLI
        else:
            importlib.reload(sys.modules['main'])

    def xtest_ratings_create(self):
        sys.argv = ['--local', '--dev', '--cli', 'r', '--job', str(root_path / 'app_local/jobs/test.ratings')]
        if 'main' not in sys.modules:
            import main     # importing will invoke the CLI
        else:
            importlib.reload(sys.modules['main'])
