from .mas_feature import AgentFeatures as Af
from .task_feature import TaskFeatures as Tf
from interface import GraphData
from utils import save_file
from typing import Dict, List
import pandas as pd


class FeatureAnalyse:
    def __init__(self, load_graph: pd.DataFrame, storage_path: str):
        self.storage_path = storage_path
        self.graph_list = load_graph

    def mas_feature(self):
        feature_list = []
        for index, row in self.graph_list.iterrows():
            graph = row['data']
            topo = row['topology']
            mas_features = Af.calculate_features(graph)
            feature_list.append({'topology': topo, 'feature': mas_features})
        df_mas_feature = pd.DataFrame(feature_list)
        save_file(df_mas_feature, f"{self.storage_path}mas_features.pkl")
        return df_mas_feature

    def task_feature(self):
        feature_list = []
        for index, row in self.graph_list.iterrows():
            graph = row['data']
            topo = row['topology']
            task_features = Tf.calculate_features(graph)
            feature_list.append({'topology': topo, 'feature': task_features})
        df_task_feature = pd.DataFrame(feature_list)
        save_file(df_task_feature, f"{self.storage_path}task_features.pkl")
        return df_task_feature

    def mas_eval(self):
        pass

    def task_eval(self):
        pass
