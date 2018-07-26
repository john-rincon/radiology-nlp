def save_object(obj, filename):
    import cPickle as pickle
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    import cPickle as pickle
    with open(filename,'rb') as input:
        loaded_object = pickle.load(input)
        return loaded_object

def save_dill_object(obj,filename):
    import dill
    with open(filename,'wb') as output:
        dill.dump(obj,output)

def load_dill_object(filename):
    import dill
    with open(filename,'rb') as input:
        loaded_object = dill.load(input)
        return loaded_object

def merge_dicts(*args):
    "Takes in list of dicts, and returns merged dictionary"
    merged_dict={}
    for dictionary in args:
        merged_dict.update(dictionary)
    return merged_dict

def find_files_in_folder(directory,extension=0):
    file_list = []
    if extension!=0:
        import os
        for file in os.listdir(directory):
            if file.endswith(extension):
                file_list.append(os.path.join(directory, file))
    else:
        for file in os.listdir(directory):
            file_list.append(os.path.join(directory,file))
    return file_list


def json_dump_tuple_key(outpath,tuple_mappings):
    "dumps tuple key dictionary in json compatible format"
    import json
    with open(outpath, 'w') as fout:
        string_tuple_mappings = {str(k): v for k, v in tuple_mappings.items()}
        json.dump(string_tuple_mappings, fout)


def json_load_tuple_key(filepath):
    "loads json files in which 'string' keys are truly tuples, converts keys back to tuples, and returns dict"
    import json
    from ast import literal_eval
    with open(filepath, 'r') as in_path:
        concept_matrix_mappings = json.load(in_path)
        concept_matrix_mappings = {literal_eval(k): v for k, v in concept_matrix_mappings.items()}
    return concept_matrix_mappings