
import sys, os, configparser
from pathlib import Path
if sys.version_info < (3,7):    # for dataclasses, etc
    raise Exception('FATAL: This app requires Python version 3.7 or later.')
# NEW: import cfcserver.app as cfcserver_app

application = None      # for uWSGI


def _run_flask_under_uwsgi():
    global application
    import cfcserver
    # app_config = _get_config_from_environ()
    cfcserver.initialize(is_prod=True)
    application = _start_flask()


def _run_flask_under_development_server():
    app_config = get_config_for_dev() if '--dev' in sys.argv \
        else _get_config_from_environ()
    app_config = {key.upper():val for key, val in app_config.items()}
    os.environ.update(**app_config)
    import cfcserver
    cfcserver.initialize(is_prod='--dev' not in sys.argv)
    flask_app = _start_flask()
    flask_app.run(debug=True)


def _run_command_line_interface():
    import ui_cli
    app_config = get_config_for_dev()
    app_config = {key.upper():val for key, val in app_config.items()}
    os.environ.update(**app_config)
    import cfcserver
    cfcserver.initialize(is_prod='--dev' not in sys.argv)
    ui_cli.application.run()
    # import ui.cli
    # app_config = get_config_for_dev() if '--dev' in sys.argv \
    #     else _get_config_from_environ()
    # cfcserver_app.initialize(**app_config)
    # ui.cli.run()


def _start_flask():
    from flask import Flask
    import ui_api, ui_http
    # import ui.api, ui.html
    flask_app = Flask(__name__.split('.')[0])
    flask_app.config['JSON_SORT_KEYS'] = False
    ui_api.initialize(flask_app)
    ui_http.initialize(flask_app)
    # ui.api.initialize(flask_app)
    # ui.html.initialize(flask_app)
    return flask_app


def _get_config_from_environ():
    required = [
        'APP_CONFIG_DIR', 'APP_DATA_DIR', 'APP_JOBS_DIR'
    ]
    undefined = [c for c in required if c not in os.environ]
    if len(undefined) > 0:
        undefined_list = ', '.join(undefined)
        raise Exception('FATAL: Undefined environment vars: ' + undefined_list)
    config = {v.lower(): os.environ.get(v, None) for v in required}
    return config


def get_config_for_dev():
    _app_local_dir = Path(__file__, '..', 'app_local').resolve()
    return dict(
        app_config_dir=str(_app_local_dir / 'config'),
        app_data_dir=str(_app_local_dir / 'data'),
        app_jobs_dir=str(_app_local_dir / 'jobs'),
    )


if __name__ != '__main__':
    _run_flask_under_uwsgi()
elif '--flask' in sys.argv:
    _run_flask_under_development_server()
else:
    _run_command_line_interface()
