##############################
# This is the main program of the application
# The goal of this application is to create an application 
# that takes as an input two YAML files, `current_version`
# and `new_version`, and updates `current_version`
##############################

import yaml
from yaml.scanner import ScannerError
import argparse
import daiquiri
import logging
import sys
from tools import *

# How deep is the YAML file
levels = 10

# Read the argument of the program given by the user
parser = argparse.ArgumentParser(description='Updates one YAML config file based on another YAML config file')
parser.add_argument('-c','--current',help='Path to current YAML file', required=True)
parser.add_argument('-n','--new',help='Path to new YAML file', required=True)
parser.add_argument('-u','--update', choices=['n', 'fu', 'ou'],help='Do you want to overwrite field ? DEFAULT n = no : no overwriting --- fu = full update : Update value of current_version by replacing the values of the currently existing fields with the values from new_version and adding or removing the fields --- ou = only update : Update value of current_version by only replacing the values of the currently existing fields with the values from new_version' ,default='n')
parser.add_argument('-v','--verbose',choices=['ERROR','INFO'],help="The level of feedback in the console, DEFAULT = ERROR",default="ERROR" )
args = vars(parser.parse_args())

# Set up the logger for the feedback messages
if args['verbose']=='ERROR':
    daiquiri.setup(level=logging.ERROR)
elif args['verbose']=='INFO':
    daiquiri.setup(level=logging.INFO)
LOG = daiquiri.getLogger()

# Open the two YAML files (current version and new version)
# Convert them into python dict object
# Check if file exists and if data are not corrupted
try: # Load current version
    LOG.info("Reading current version YAML file")
    current = read(args['current'])       
except FileNotFoundError:
    LOG.error("The path to the current version YAML file is incorrect")
    sys.exit(0)
except ScannerError:
    LOG.error("The data in the current version YAML are corrupted, check data integrity")
    sys.exit(0)

try: # Load new version
    LOG.info("Reading new version YAML file")
    new = read(args['new'])
except FileNotFoundError:
    LOG.error("The path to the new version YAML file is incorrect")
    sys.exit(0)
except ScannerError:
    LOG.error("The data in the new version YAML are corrupted, check data integrity")
    sys.exit(0)

# Test that files are not empty
try:
    if(not bool(current)):
        raise Exception
except:
    LOG.error("The current version YAML file is empty")
    sys.exit(0)
try:
    if(not bool(new)):
        raise Exception
except:
    LOG.error("The new version YAML file is empty")
    sys.exit(0)

# OBJECTIVES
# - If a field of `new_version` is not present in `current_version`, it should be
#   added to `current_version` with its value set to the value from `new_version`.
# - If a field of `new_version` is present in `current_version`, it should keep the
#   value from `current_version`.
# - If a field of `current_version` is not present in `new_version`, it should be
#   removed from `current_version`

# Different use case of the application
if args['update']=='fu': #- Force the update of `current_version` by replacing the values 
    # of the currently existing fields with the values from `new_version` and adding or 
    # removing the fields according to the requirement mentioned above 
    LOG.info('The chosen scenario is full update')
    recursive_merge(current, new, levels) #Add new fields
    recursive_remove(current,new,levels) #Remove old fields
    current.update(new) #Update data contained in both YAML file

elif args['update']=='ou': #- Force the update of `current_version` by only 
    # replacing the values of the currently existing fields with the values from `new_version`
    LOG.info('The chosen scenario is only update')
    keys=[] # Store keys of hte current version YAML file
    keys = recursive_keys(current,keys) # Get all the keys
    current = update(current,new,keys) # Update common fields

else: #- No update, only adding or removing the fields according to the requirement mentioned above 
    LOG.info('The chosen scenario is no update')
    recursive_merge(current, new, levels) #Add new fields
    recursive_remove(current,new,levels) #Remove old fields

# Overwrite the current version YAML file with the result of the application
try:
    with open(args['current'], 'w') as write_file:
        LOG.info("Writing result is the current version YAML file")
        yaml.dump(current, write_file, sort_keys=False)
except:
    LOG.error("There is an error when overwriting the current version YAML file, check the file permissions")
    sys.exit(0)

