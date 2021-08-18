#!/usr/bin/python

import pickle

import pandas as pd

object = pd.read_pickle(r'filepath')
print(object)

with open('topple.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)