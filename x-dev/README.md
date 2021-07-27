# CFC Server

For technical notes, see
[GDOC](https://docs.google.com/document/d/11xfUCICvy3dSOLOvE1uH1STvy8lWfX3qKThimBQEFQM/edit#).

## Setup
CFC Server runs within a Python virtual environment.
The virtual environment must be created at install-time.
and activated at run-time.
* For Flask Development Server (on laptop)
  * Intellij: In every run configuration, including starting the Flask
    development server, check options for "Add content roots to PYTHONPATH"
    and "Add source roots to PYTHONPATH".

### uWSGI - Production / Opalstack.com
* For production on opalstack.com
* To activate the Python virtual environment, the uWSGI .ini file
  has `virtualenv = /path/to/cfc-server/deployed/venv`

### IntelliJ - Development
* Get code from Gitlab
  * `git clone ...`
* Create Python virtual environment
  * Windows: `py -3.9 -m venv venv --prompt cfc-server`
* Install Python libraries: Do ONE of the following:
  * Option 1: When not adding or upgrading libraries, use the current
    "frozen" levels as defined in `requirements.frozen.txt`.
    * `venv\Scripts\activate`
    * `pip3 install -r .\x-dev\python\requirements.frozen.txt`

* Install required Python libraries:
  * `venv\Scripts\activate`
  * `pip3 install -r .\x-dev\python\requirements.frozen.txt`
* Install a NEW required Python library:
  * `py -m pip install SQLAlchemy -t .\lib\python3.8`
  * `py -m pip freeze --path .\lib\python3.8 > .\x-dev\python\requirements.frozen.txt`

### Command Line
* To activate the Python virtual environment, before invoking the command:
  * Linux: run `source venv/bin/activate`
  * Windows: run `venv/Scripts/activate`


## Setup - Developer Laptop
* IDE Settings:
  * Intellij path variables: $PROJECT_DIR$
  * File > Project Structure > SDKs: add path ...\lib\python3.8
  * Use Unix/Mac line endings (\n). Intellij: File > Settings > Editor > Code Style: line separator.


# @@@@ WEBFACTION SETUP @@@@
### Apache and mod_wsgi
apached/conf/httpd.conf:
```text
WSGIDaemonProcess cfc_server processes=1 threads=12 python-path=/home/swo/webapps/cfc_server/lib/python3.8 python-home=/home/swo/webapps/cfc_server/venv
WSGIProcessGroup cfc_server
WSGIScriptAlias / /home/swo/webapps/cfc_server/wsgi.py process-group=cfc_server application-group=%{GLOBAL}
WSGIRestrictEmbedded On
WSGILazyInitialization On
```
* Above configuration started with Webfactions default config for mod_wsgi.
* To use a Python virtual environment,
  [THIS]((https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html))
  said to add `python-home=...` to `WSGIDaemonProcess`.
* To use a Python virtual environment, 
  [THIS]
  says to replace `python-path=...`
  with `python-home=/absolute/path/to/myproject/venv`
* To reduce start-up time,
  [THIS](https://docs.webfaction.com/software/mod-wsgi.html)
  said to add `process-group=<app> application-group=%{GLOBAL}` to `WSGIScriptAlias`.

References:
* [mod_wsgi doc](https://modwsgi.readthedocs.io/)
* [mod_wsgi doc - virtual envs](https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html)

### Flask
References:
* [Flask 1.1.x doc](https://flask.palletsprojects.com/en/1.1.x/)
