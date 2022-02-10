EPSILON = ''
import pickle

def make_pickle_file(filename, data):
    with open(f"{filename}.pickle", "wb") as outfile:
        pickle.dump(data, outfile)

def unpick_pickle_file(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    
    return data