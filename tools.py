import yaml
######################
# This is the python file containing all the functions
# used for the application by the main file
######################

# Add new field to current version based on new version without overwriting 
# the value from current version
# Parameters :
    # - dict_a : data of the current version YAML file (will be updated)
    # - dict_b : data of the new version YAML file
    # - levels : depth of the YAML file
def recursive_merge(dict_a, dict_b, levels):
    for k, v in dict_b.items():
        if k in dict_a:
            if levels > 1 and isinstance(v, dict) and isinstance(dict_a[k], dict):
                recursive_merge(dict_a[k], dict_b[k], levels - 1)
            else:
                pass #keep the value from dict_a
        else:
            dict_a[k] = v

# Remove element that are in current version but not in new version
# Parameters :
    # - dict_a : data of the current version YAML file (will be updated)
    # - dict_b : data of the new version YAML file
    # - levels : depth of the YAML file
def recursive_remove(dict_a,dict_b,levels):
    for k,v in dict_a.copy().items():
        if k in dict_b:
            if levels > 1 and isinstance(v, dict) and isinstance(dict_a[k], dict):
                recursive_remove(dict_a[k], dict_b[k], levels - 1)
            else:
                pass #keep the value from dict_a
        else:
            dict_a.pop(k)

# Get all the keys of the current version YAML file
# Parameters :
    # - dictionnary : data of the current version YAML file
    # - keys : list to store the keys 
# Return :
    # - keys : list with all the keys  
def recursive_keys(dictionary,keys):
    for key, value in dictionary.items():
        if type(value) is dict:
            keys.append(key)
            recursive_keys(value,keys)
        else:
            keys.append(key)
    return keys

# Update the values of current version with the ones from new version
# Parameters :
    # - dict_a : data of the current version YAML file (will be updated)
    # - dict_b : data of the new version YAML file
    # - keys : list with all the keys of current version
def update(dict_a,dict_b,keys):
    for k, v in dict_b.items():
        if k in keys:
            if isinstance(v, dict):
                dict_a[k] = update(dict_a.get(k, {}), v,keys)
            else:
                dict_a[k] = v
    return dict_a
# Read the YAML file to store the data into python dict object
# Parameters :
    # - path_yaml : path to the yaml file
# Return :
    # - dict : dictionnary with data from YAML file
def read(path_yaml):
    with open(path_yaml, 'r',encoding='utf8') as fp:
        dict = yaml.safe_load(fp)
        return dict 
