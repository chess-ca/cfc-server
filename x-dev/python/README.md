# CFC Server - Python

## Venv & Packages

* CFC Server runs within a Python virtual environment (venv)
  for all invocation types: uWSGI (Prod); Flask's built-in server (Dev);
  and command line.
    * At install-time, the virtual environment must be created
      and required Python packages must be installed.
    * At run-time, the virtual environment must be activated.

### Re-installing and Re-versioning All Packages

* When adding or upgrading libraries, update and install the
  "base" dependencies at versions defined in `requirements.base.txt`.
  Install these "base" dependencies, which will also install secondary dependencies
  as required.  Then "freeze" all these (so that all developers can have packages
  at the same version level).
* Steps:
  * Update `requirements.base.txt` to add a new Python package or
    to change the version of an existing Python package (upgrade).
  * Close IntelliJ. If `.\venv` is deleted or renamed while IntelliJ is running,
    it will reset the configuration of its Python Interpreter / SDK (and won't
    find installed packages for auto-complete).
  * Delete the `.\venv` directory
  * `py -3.9 -m venv venv --prompt cfc-server`
  * `venv\Scripts\activate`
  * `pip3 install -r .\x-dev\python\requirements.base.txt`
  * `pip3 freeze > .\x-dev\python\requirements.frozen.txt`
