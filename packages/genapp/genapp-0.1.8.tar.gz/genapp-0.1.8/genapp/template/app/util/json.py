def merge_json(obj1, obj2):
    """
    Merge two JSON objects recursively.
    """
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        merged = obj1.copy()
        for key, value in obj2.items():
            if key in merged:
                merged[key] = merge_json(merged[key], value)
            else:
                merged[key] = value
        return merged
    elif isinstance(obj1, list) and isinstance(obj2, list):
        return obj1 + obj2
    elif obj1 != obj2:
        # If both objects are not dictionaries or lists and are different,
        # return a list containing both values
        return [obj1, obj2]
    else:
        # If both objects are not dictionaries or lists and are the same,
        # return either one
        return obj1
    
def rename_key_in_list_of_dicts(list_of_dicts, old_key, new_key):
    """
    Renames a key in a list of dictionaries.

    Parameters:
    - list_of_dicts (list): List of dictionaries where key needs to be renamed.
    - old_key (str): Old key name.
    - new_key (str): New key name.

    Returns:
    - list: Modified list of dictionaries with the key renamed.
    """
    for item in list_of_dicts:
        if old_key in item:
            item[new_key] = item.pop(old_key)
    return list_of_dicts

def combine_entries(list_, ident, key_to_combine):
    combined_dict = {}
        
    for element in list_:
        key = element[ident]
            
        if key not in combined_dict:
            combined_dict[key] = element
            combined_dict[key][key_to_combine] = [element[key_to_combine]]
        else:
            combined_dict[key][key_to_combine].append(element[key_to_combine])
        
    # Convert the dictionary back to a list
    return list(combined_dict.values())
