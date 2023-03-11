##############################
# This is the test program of the application
# The goal of this to test the differents functions
# and use case scenario
##############################

import pytest
import yaml
from tools import *

#########################
# Init
#########################

@pytest.fixture
def levels():
    return 10
@pytest.fixture
def keys():
    return []
@pytest.fixture
def dict_a():
    return dict({"a":1,
                 "b":2,
                 "c":3})
@pytest.fixture
def dict_b():
    return dict({"a":2,
                 "b":2,
                 "d":3})
@pytest.fixture
def dict_a_nested():
    return dict({"a":{"A":1},
                 "b":2,
                 "c":{"B":{"C":3,"F":7},
                      "D":4}})
@pytest.fixture
def dict_b_nested():
    return dict({"a":{"A":2},
                 "b":1,
                 "c":{"B":{"C":4,"G":3},
                      "E":4}})

#########################
# Unit tests
#########################

# Simple dict
def test_recursive_merge_simple(dict_a,dict_b,levels):
    answer = dict({'a': 1, 'b': 2, 'c': 3, 'd': 3})
    recursive_merge(dict_a,dict_b,levels)
    assert dict_a == answer
def test_recursive_remove_simple(dict_a,dict_b,levels):
    answer = dict({"a":1,"b":2})
    recursive_remove(dict_a,dict_b,levels)
    assert dict_a == answer
def test_recursive_keys_simple(dict_a,keys):
    answer = ["a","b","c"]
    test = recursive_keys(dict_a,keys)
    assert test == answer
def test_update_simple(dict_a,dict_b,keys):
    answer = dict({"a":2,"b":2,"c":3})
    keys = recursive_keys(dict_a,keys)
    dict_a = update(dict_a,dict_b,keys)
    assert dict_a == answer

# Nested dict
def test_recursive_merge_nested(dict_a_nested,dict_b_nested,levels):
    answer = dict({"a":{"A":1},
                 "b":2,
                 "c":{"B":{"C":3,"F":7,"G":3},
                      "D":4,
                      "E":4}})
    recursive_merge(dict_a_nested,dict_b_nested,levels)
    assert dict_a_nested == answer
def test_recursive_remove_nested(dict_a_nested,dict_b_nested,levels):
    answer = dict({"a":{"A":1},
                 "b":2,
                 "c":{"B":{"C":3}}})
    recursive_remove(dict_a_nested,dict_b_nested,levels)
    assert dict_a_nested == answer
def test_recursive_keys_nested(dict_a_nested,keys):
    answer = ["a","A","b","c","B","C","F","D"]
    test = recursive_keys(dict_a_nested,keys)
    assert test == answer
def test_update_nested(dict_a_nested,dict_b_nested,keys):
    answer = dict({"a":{"A":2},
                 "b":1,
                 "c":{"B":{"C":4,"F":7},
                      "D":4}})
    keys = recursive_keys(dict_a_nested,keys)
    dict_a_nested = update(dict_a_nested,dict_b_nested,keys)
    assert dict_a_nested == answer

# Other unit tests
def test_read():
    path = "./yaml/test_read.yaml"
    dictionnary = read(path)
    answer = dict({"picking":
                        {"max_error":
                            {"bottle":[0.001,0.001,0.001]}},
                    "error_msgs":
                        {"impossible_move":
                            {"en":"Robot cannot perform the requested move"}}})
    assert dictionnary == answer

#########################
# Exception raised tests
#########################

def test_empty_exception():
    with pytest.raises(Exception) as e:
        path = "./yaml/test_empty_file.yaml"
        dictionnary = read(path)
        if(not bool(dictionnary)):
            raise Exception

def test_file_exists_exception():
    with pytest.raises(FileNotFoundError) as e:
        path = "./yaml/xxxxxxxxxxxxxxx.yaml"
        dictionnary = read(path)

def test_file_data_integrity_exception():
    with pytest.raises(yaml.scanner.ScannerError) as e:
        path = "./yaml/test_wrong_syntax.yaml"
        dictionnary = read(path)

#########################
# End to end tests
#########################

#Case 1 : Add - Remove
def test_case_ADD_REMOVE(levels):
    current = read("yaml/case1_current.yaml")
    new = read("yaml/case1_new.yaml")
    answer = read("yaml/case1_answer.yaml")
    recursive_merge(current, new, levels) #Add new fields
    recursive_remove(current,new,levels) #Remove old fields
    assert current == answer

#Case 2 : Update
def test_case_UPDATE(keys):
    current = read("yaml/case2_current.yaml")
    new = read("yaml/case2_new.yaml")
    answer = read("yaml/case2_answer.yaml")
    keys = recursive_keys(current,keys) # Get all the keys
    current = update(current,new,keys) # Update common fields
    assert current == answer

#Case 3 : Add - Remove - Update
def test_case_ADD_REMOVE_UPDATE(levels):
    current = read("yaml/case3_current.yaml")
    new = read("yaml/case3_new.yaml")
    answer = read("yaml/case3_answer.yaml")
    recursive_merge(current, new, levels) #Add new fields
    recursive_remove(current,new,levels) #Remove old fields
    current.update(new) #Update data contained in both YAML file
    assert current == answer