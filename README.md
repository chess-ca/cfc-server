# CFC-server

This is the back-end server for the Chess Federation of Canada (CFC) located at server.chess.ca.
* Has APIs called by the CFC website for dynamic data (ratings, etc).
* Has files (in a different Gitlab repo) accessed via the CFC website. 
* Has a website for CFC Business Office administrative tasks and reports.

## Setup
See [x-dev/README](x-dev/README.md) for details.

## Running
See [x-dev/README](x-dev/README.md) for details.  In summary, ...

* Development:
  * Activating a Python virtual environment is NOT required.
  * The `flask:run` NPM task runs the start-up:
    * Sets `FLASK_ENV` to "development"
    * Invokes `python cfc_server.py` (will run as a local server)
      * Sets environment vars `APP_CONFIR_DIR` and `APP_DATA_DIR`. 

* Production:
  * The `uwsgi.ini` config file defines the start-up:
    * Sets environment vars `APP_CONFIR_DIR` and `APP_DATA_DIR`.
    * Invokes `deployed/cfc_server.py` (will run as a UWSGI app)
  * Upgrading to the last code:
    * Run `python3 deploy.py`.  This will ...
      * Creates the next available deploy directory (seq# + 1);
      * git clones the code from the Gitlab repos;
      * pip installs the libraries (using requirements.frozen.txt);
      * sets the `deployed` soft link to the new deploy directory;
      * reloads UWSGI.
