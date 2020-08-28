# CFC-Server

## WSGI Start-Up

### Overview

#### Deploy

#### Startup

On Webfaction (should be similar elsewhere), the start-up process is:
* As part of its environment for mod_wsgi, Webfaction has a cron job that
  will start Apache2 if it is not already running.
* Apache2 starts mod_wsgi which is configured to call ./wsgi-start.py.
* ./wsgi-start.py does the minimum to load `application` from cfc_server.py.
  * Sets environment variables specific to the server environment:
    * `APP_CONFIG_ROOT` - location of app.config
    * `APP_DATA_ROOT` - location of SQLite databases, etc.
  * Reads the file wsgi-start.current-deploy.txt
    to get the name of the directory of the currently deployed code.
  * Adds that deploy directory to Python's `sys.path`.
  * from cfc_server imports application.
* ./deploy-0001/cfc_server.py