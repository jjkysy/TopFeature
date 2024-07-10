import os
import pickle
from typing import List
import pandas as pd


def save_file(file: pd.DataFrame, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file.to_pickle(filename)


def load_file(filename):
    return pd.read_pickle(filename)
