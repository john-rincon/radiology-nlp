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




