
import sys, os
if sys.version_info < (3,7):    # for dataclasses, etc
    raise Exception('FATAL: This app requires Python version 3.7 or later.')
from pathlib import Path

application = None      # for uWSGI
_config_file_env_var = 'CFCSERVER_CONFIG_FILE'
_app_root_dir = Path(__file__).resolve().parent


def main():
    if __name__ != '__main__':
        _run_flask_with_uwsgi()
    elif '--flask' in sys.argv:
        _run_flask_with_development_server()
    else:
        _run_command_line_interface()


def _run_flask_with_uwsgi():
    global application
    import cfcserver
    cfcserver.initialize(get_config_file())
    application = _initialize_flask()


def _run_flask_with_development_server():
    import cfcserver
    cfcserver.initialize(get_config_file())
    if '--dev' in sys.argv:
        # Ref: https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = '1'
    flask_app = _initialize_flask()
    flask_app.run()


def _run_command_line_interface():
    import cfcserver
    cfcserver.initialize(get_config_file())
    import ui.cli as ui_cli
    ui_cli.run()


def _initialize_flask():
    from flask import Flask
    import ui.api, ui.html
    flask_app = Flask(__name__.split('.')[0])
    flask_app.config['JSON_SORT_KEYS'] = False
    ui.api.initialize(flask_app)
    ui.html.initialize(flask_app)
    return flask_app


def get_config_file():
    app_config_file = os.environ.get(_config_file_env_var, None)
    if '--local' in sys.argv or app_config_file is None:
        app_config_file = str(_app_root_dir / 'app_local' / 'config' / 'app.config')
    if not Path(app_config_file).exists():
        raise Exception('FATAL: App config file not found: ' + (app_config_file or '(unspecified)'))
    return app_config_file


main()
