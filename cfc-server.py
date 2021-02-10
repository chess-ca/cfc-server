
import sys, os
from pathlib import Path

application = None


def main():
    global application
    root_dir = Path(__file__).parent

    _check_python_version()
    _add_to_python_path(root_dir)
    if __name__ != '__main__':
        # ---- Start Flask Prod/UWSGI
        application = _start_flask()
        import cfcserver
        cfcserver.initialize(is_prod=True)
    else:
        _set_environ_vars(root_dir)
        import cfcserver
        cfcserver.initialize(is_prod='--dev' not in sys.argv)
        if len(sys.argv) <= 1:
            # ---- Start Flask in Dev/Local
            application = _start_flask()
            application.run(debug=True)
        else:
            # ---- Start Command Line
            import ui_cli
            ui_cli.application.run()


def _check_python_version():    # Requires Python 3.7+ (dataclasses, ...)
    if sys.version_info < (3,7):
        sys.exit('FATAL: Python version 3.7 or later is required by this app.')


def _add_to_python_path(root_dir):
    py_version = f'{sys.version_info[0]}.{sys.version_info[1]}'
    pylib_dir = root_dir / 'lib' / f'python{py_version}'
    if not pylib_dir.exists():
        print(f'ERROR: Python library directory not found: {pylib_dir}')
        exit(9903)
    sys.path.insert(0, str(pylib_dir))
    sys.path.insert(0, str(root_dir))


def _set_environ_vars(root_dir):    # For Development
    os.environ.update(
        APP_CONFIG_DIR=str(root_dir / 'app_local' / 'config'),
        APP_DATA_DIR=str(root_dir / 'app_local' / 'data'),
        APP_JOBS_DIR=str(root_dir / 'app_local' / 'jobs'),
    )


def _start_flask():
    global application
    from flask import Flask         # imported only if needed
    import ui_api, ui_http

    flask_app = Flask(__name__.split('.')[0])
    flask_app.config['JSON_SORT_KEYS'] = False
    ui_api.initialize(flask_app)
    ui_http.initialize(flask_app)
    return flask_app


main()
