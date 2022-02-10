EPSILON = ''
import pickle
from os import path, mkdir
from typing import Any, Tuple

def make_pickle_file(file_name, data):
    with open(f"{file_name}.pickle", "wb") as outfile:
        pickle.dump(data, outfile)

def unpick_pickle_file(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    
    return data

def serialize_data(data, file_name: str):
    if not path.exists('./serialized_data'):
        mkdir('./serialized_data')

    make_pickle_file(file_name, data)

def deserialize_data(file_name) -> Tuple[bool, Any]:
    if path.exists(file_name):
        data = unpick_pickle_file(file_name)
        return data
    
    else: return None