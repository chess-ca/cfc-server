
import sys, pathlib

app_dir = str(pathlib.Path(__file__).parent)
sys.path.insert(0, app_dir)

from flask import Flask
import app, ui_api, ui_html

flask_app = Flask(__name__.split('.')[0])
application = flask_app       # for mod_wsgi

is_prod = (__name__ != '__main__')
flask_app.config['JSON_SORT_KEYS'] = False

app.initialize(is_prod)
ui_api.initialize(flask_app)
ui_html.initialize(flask_app)

if __name__ == '__main__':
    flask_app.run(debug=True)
