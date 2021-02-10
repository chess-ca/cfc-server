# CFC Server

For technical notes, see
[GDOC](https://docs.google.com/document/d/11xfUCICvy3dSOLOvE1uH1STvy8lWfX3qKThimBQEFQM/edit#).

## Setup - Production

## Setup - Development
* Install required Python libraries:
  * `py -m pip install -r .\x-dev\python\requirements.frozen.txt -t .\lib\python3.8`
* Install a NEW required Python library:
  * `py -m pip install SQLAlchemy -t .\lib\python3.8`
  * `py -m pip freeze --path .\lib\python3.8 > .\x-dev\python\requirements.frozen.txt`


## Setup - Developer Laptop
* IDE Settings:
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
