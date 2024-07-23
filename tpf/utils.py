import csv
import os
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def calculate_hits(needles, target_hole):
    return [needle for needle in needles if target_hole.contains(needle)]


def save_file(file: pd.DataFrame, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file.to_pickle(filename)


def save_as_csv(file: pd.DataFrame, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file.to_csv(filename, index=False)


def load_file(filename):
    return pd.read_pickle(filename)


def pkl_2_csv(filename):
    csv_filename = filename[:-4] + ".csv"
    with open(csv_filename, "rb", newline="") as f:
        data = pickle.load(f)
        with open(filename[:-4] + ".csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(data[0].__dict__.keys())
            for d in data:
                writer.writerow(d.__dict__.values())
    return csv_filename


class PlotStorage:
    def __init__(self, path: str):
        sns.set_theme(style="whitegrid")
        self.path = path

    def save_plot(self, name: str):
        full_path = os.path.join(self.path, f"{name}.png")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        plt.savefig(full_path)
        plt.close()
