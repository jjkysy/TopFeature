import os
import pickle
from typing import List
import pandas as pd
import csv


def save_file(file: pd.DataFrame, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file.to_pickle(filename)

def load_file(filename):
    return pd.read_pickle(filename)

def pkl_2_csv(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
        with open(filename[:-4] + ".csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(data[0].__dict__.keys())
            for d in data:
                writer.writerow(d.__dict__.values())
    return filename[:-4] + ".csv"