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

import sys, os, logging
if sys.version_info < (3,7):    # 3.7+ for dataclasses; 3.6+ for f-strings; ...
    raise Exception('Python version 3.7 or later is required')
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
        raise Exception('Invalid run mode. Invoke with --cli, --flask, or from uWSGI')


def _run_flask_with_uwsgi():
    """Run App with Flask and uWSGI (production)"""
    global application
    import cfcserver
    cfcserver.initialize(get_config_file())
    application = _initialize_flask()


def _run_flask_with_development_server():
    """Run App with Flask's built-in server (development)"""
    import cfcserver
    cfcserver.initialize(get_config_file())
    if '--dev' in sys.argv:
        # Ref: https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = '1'
    flask_app = _initialize_flask(is_dev=True)
    flask_app.run()


def _run_command_line_interface():
    """Run App with command line interface (background jobs)"""
    import cfcserver
    cfcserver.initialize(get_config_file())
    import cfcserver.ui.cli as ui_cli
    ui_cli.run()


def _initialize_flask(is_dev=False):
    from flask import Flask
    flask_app = Flask(__name__.split('.')[0])
    flask_app.static_folder = 'cfcserver/static'
    flask_app.config['JSON_SORT_KEYS'] = False
    flask_app.config['UPLOAD_FOLDER'] = r'C:\_\IT\Projects\CFC\CFC-Server\CFC-server.Code\app_local\tmp'
    flask_app.secret_key = os.environ.get('APP_SECRET_KEY', 'secret-for-dev-only')
    flask_app.context_processor(lambda: dict(is_dev=is_dev))

    import cfcserver.ui.api as ui_api
    import cfcserver.ui.html as ui_html
    ui_api.initialize(flask_app)
    ui_html.initialize(flask_app)
    return flask_app


def get_config_file():
    if '--local' in sys.argv:
        config_file = _app_root_dir / 'app_local/config/app.config.ini'
    elif _config_file_env_var not in os.environ:
        raise Exception('Set environment var "{}" or use --local'.format(_config_file_env_var))
    else:
        config_file = Path(os.environ.get(_config_file_env_var)).resolve()
    if not config_file.exists():
        raise FileNotFoundError('Config file not found: ' + (config_file or '(unspecified)'))
    return str(config_file)


main()
