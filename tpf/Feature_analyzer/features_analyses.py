import pandas as pd
from utils import save_file

from .mas_feature import AgentFeatures as Af
from .mas_feature_eval import MASFeatureEvaluator as Mfe
from .task_feature import TaskFeatures as Tf
from .task_feature_eval import TaskFeatureEvaluator as Tfe


class FeatureAnalyse:
    def __init__(self, load_graph: pd.DataFrame, storage_path: str):
        self.storage_path = storage_path
        self.graph_list = load_graph

    def mas_feature(self):
        feature_list = []
        for index, row in self.graph_list.iterrows():
            graph = row["data"]
            topo = row["topology"]
            mas_features = Af.calculate_features(graph)
            feature_list.append({"topology": topo, "feature": mas_features})
        df_mas_feature = pd.DataFrame(feature_list)
        save_file(df_mas_feature, f"{self.storage_path}mas_features.pkl")
        return df_mas_feature

    def task_feature(self):
        feature_list = []
        for index, row in self.graph_list.iterrows():
            graph = row["data"]
            topo = row["topology"]
            task_features = Tf.calculate_features(graph)
            feature_list.append({"topology": topo, "feature": task_features})
        df_task_feature = pd.DataFrame(feature_list)
        save_file(df_task_feature, f"{self.storage_path}task_features.pkl")
        return df_task_feature


class FeatureEval:
    def __init__(self, load_feature: pd.DataFrame, storage_path: str):
        self.storage_path = storage_path
        self.feature_list = load_feature

    def mas_eval(self):
        evaluation_list = []
        for index, row in self.feature_list.iterrows():
            features = row["feature"]
            topo = row["topology"]
            mas_eval = Mfe.evaluate_graph(features)
            evaluation_list.append({"topology": topo, "evaluation": mas_eval})
        df_mas_eval = pd.DataFrame(evaluation_list)
        save_file(df_mas_eval, f"{self.storage_path}mas_eval.pkl")
        return df_mas_eval

    def task_eval(self):
        evaluation_list = []
        for index, row in self.feature_list.iterrows():
            features = row["feature"]
            topo = row["topology"]
            task_eval = Tfe.evaluate_graph(features)
            evaluation_list.append({"topology": topo, "evaluation": task_eval})
        df_task_eval = pd.DataFrame(evaluation_list)
        save_file(df_task_eval, f"{self.storage_path}task_eval.pkl")
        return df_task_eval

    # TODO: simplify the code by combining the two methods
