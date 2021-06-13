'''Main entry point to start the application from either a uWSGI server (for prod),
Flasks built-in .run (for dev), or CLI (Python command line interface for batch).

Args:
    --flask: run the Flask dev environ.
    --dev: use settings for development.
    --local: use the local development environ's config file.
    (other args for CLI: see ui/cli/run.py:_parse_args()
Environment Variables:
    CFCSERVER_CONFIG_FILE: if not --local, it's the app's configuration file.
'''

import sys, os, logging
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
    if '--local' in sys.argv:
        app_config_file = str(_app_root_dir / 'app_local/config/app.config')
    elif _config_file_env_var not in os.environ:
        raise ValueError('FATAL: Set environment var "{}" or use --local'.format(_config_file_env_var))
    else:
        app_config_file = os.environ.get(_config_file_env_var)
    if not Path(app_config_file).exists():
        raise FileNotFoundError('FATAL: App config file not found: ' + (app_config_file or '(unspecified)'))
    logging.info('Using app config file: %s', app_config_file)
    return app_config_file


main()
