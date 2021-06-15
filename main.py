"""
Start the application to run either with (1) uWSGI server (for prod), (2) Flask's
built-in dev server (for dev), or (3) Python's command line interface (for batch).

Environment Variables:
    CFCSERVER_CONFIG_FILE: App's configuration file (required if not --local)

Args:
    --flask: run with Flask's built-in dev server.
    --dev: use settings for development.
    --local: config file is in the local development environ.
    (other args for CLI: see ui/cli/run.py:_parse_args()
"""

import sys, os
if sys.version_info < (3,7):    # for dataclasses, f-strings (3.6), etc
    raise Exception('FATAL: This app requires Python version 3.7 or later.')
from pathlib import Path

_config_file_env_var = 'CFCSERVER_CONFIG_FILE'
_app_root_dir = Path(__file__).resolve().parent

application = None      # Used by uWSGI


def main():
    if '--cli' in sys.argv:
        _run_command_line_interface()
    elif '--flask' in sys.argv:
        _run_flask_with_development_server()
    elif __name__ != '__main__':
        _run_flask_with_uwsgi()
    else:
        raise Exception('Invalid run mode. Was not CLI (--cli), Flask (--flask), or uWSGI')


def _run_flask_with_uwsgi():
    '''Run App in uWSGI and Flask (production)'''
    global application
    import cfcserver
    cfcserver.initialize(get_config_file())
    application = _initialize_flask()


def _run_flask_with_development_server():
    '''Run App in Flask.run() (development)'''
    import cfcserver
    cfcserver.initialize(get_config_file())
    if '--dev' in sys.argv:
        # Ref: https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = '1'
    flask_app = _initialize_flask()
    flask_app.run()


def _run_command_line_interface():
    '''Run App in command line interface (background jobs)'''
    import cfcserver
    cfcserver.initialize(get_config_file())
    import cfcserver.ui.cli as ui_cli
    ui_cli.run()


def _initialize_flask():
    from flask import Flask
    import cfcserver.ui.api
    import cfcserver.ui.html as ui_html
    flask_app = Flask(__name__.split('.')[0])
    flask_app.config['JSON_SORT_KEYS'] = False
    cfcserver.ui.api.initialize(flask_app)
    ui_html.initialize(flask_app)
    return flask_app


def get_config_file():
    if '--local' in sys.argv:
        config_file = str(_app_root_dir / 'app_local/config/app.config.ini')
    elif _config_file_env_var not in os.environ:
        raise ValueError('FATAL: Set environment var "{}" or use --local'.format(_config_file_env_var))
    else:
        config_file = os.environ.get(_config_file_env_var)
    if not Path(config_file).exists():
        raise FileNotFoundError('FATAL: Config file not found: ' + (config_file or '(unspecified)'))
    return config_file


main()
