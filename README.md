# Documentation

The goal of this project is to create an application that takes as an input two YAML files, `current_version` and `new_version`, and updates `current_version` as follows:
- If a field of `new_version` is not present in `current_version`, it should be
  added to `current_version` with its value set to the value from `new_version`.
- If a field of `new_version` is present in `current_version`, it should keep the
  value from `current_version`.
- If a field of `current_version` is not present in `new_version`, it should be
  removed from `current_version`.

Furthermore there is an optional argument to overwrite the common data to both files.

## How to install

In a python 3.8.0 environment :
    pip install -r requirements.txt \
This command will install the dependencies used for this project.
If there are problems, try to uncomment the commented dependencies in the requirements.txt file and launch the command again.

## Description

This project is composed of 
- 3 python files
  - main_app.py : This is the main file that launch the app
  - tools.py : This file contains various useful functions for the app
  - test.py : This file contains all the tests for this app
- 2 YAML files at the same level as the python files
- A directory containing YAML files used in the tests

## How to use

### Launch the app

Command for help : python main_app.py -h \
The main app python script takes multiple arguments :
- -c (--current) : the path to the current YAML file (REQUIRED)
- -n (--new) : the path to the new YAML file (REQUIRED)
- -u (--update) : the use case of the app 
  - n : no overwriting, only adding and removing new and old fields (DEFAULT)
  - fu : full update, update values currently existing, add and remove new and old fields
  - ou : only update, update values currently existing without adding or removing new and old fields
- -v (--verbose) : the logging level
  - ERROR : show only error messages (DEFAULT)
  - INFO : show error messages and info messages

Example :
python main_app.py -c motor_config_current.yaml -n motor_config_new.yaml -u fu -v INFO
### Launch the tests

Command to launch the tests with PYTEST : pytest test.py \
There are a total of 15 tests (unit, exception and end to end tests)
