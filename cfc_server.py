
import sys, os
from pathlib import Path

if sys.version_info < (3,7):
    # App needs Python 3.7+ (dataclasses, ...)
    sys.exit('FATAL: Python version 3.7 or later is required by this app.')

# ---- Add this deploy's libraries to Python's path
_py_version = f'{sys.version_info[0]}.{sys.version_info[1]}'
_root_dir = Path(__file__).parent
_pylib_dir = Path(_root_dir, 'lib', f'python{_py_version}')
if not _pylib_dir.exists():
    print(f'ERROR: Python library directory not found: {_pylib_dir}')
    exit(9903)
sys.path.insert(0, str(_pylib_dir))
sys.path.insert(0, str(_root_dir))

# ---- Add environment variables (required before importing app)
if __name__ == '__main__':
    os.environ.update(
        APP_CONFIG_DIR=str(_root_dir / 'private' / 'config'),
        APP_DATA_DIR=str(_root_dir / 'private' / 'data'),
    )

# ---- Flask start-up
from flask import Flask
import cfcserver, ui_api, ui_http

flask_app = Flask(__name__.split('.')[0])
application = flask_app       # for mod_wsgi

is_prod = (__name__ != '__main__')
flask_app.config['JSON_SORT_KEYS'] = False

cfcserver.initialize(is_prod)
ui_api.initialize(flask_app)
ui_http.initialize(flask_app)

if __name__ == '__main__':
    flask_app.run(debug=True)
