# tests README

To run the tests from the command line:
* `cd c:\path\to\root\of\project`
* `venv\scripts\activate`
* `python -m unittest`

To run the tests from IntelliJ:
* Create a run configuration of type "Python tests" > "Unittests"
  pointing to the ./tests directory.
  * Check options for both "Add content roots to PYTHONPATH"
    and "Add source roots to PYTHONPATH"  
* Run the tests from within IntelliJ
