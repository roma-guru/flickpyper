from os import path
import pickle

def get_ids(file):
    if path.isfile(file):
        with open(file, 'rb') as f:
            return pickle.load(f)
    else:
        return []

def put_ids(file, ids):
    with open(file, 'wb') as f:
        pickle.dump(ids, f)

