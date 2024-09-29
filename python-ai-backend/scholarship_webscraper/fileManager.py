# fileManager.py

import pickle
import os


def readSet(filename):
    """Read a set from a pickle file."""
    if not os.path.exists(filename):
        return set()
    with open(filename, 'rb') as file:
        return pickle.load(file)


def storeSet(filename, data_set):
    """Store a set to a pickle file."""
    with open(filename, 'wb') as file:
        pickle.dump(data_set, file)


def appendToSet(filename, item):
    """Append an item to a set stored in a pickle file."""
    current_set = readSet(filename)
    current_set.add(item)
    storeSet(filename, current_set)
