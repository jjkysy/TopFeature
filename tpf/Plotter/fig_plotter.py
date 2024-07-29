##############################################################################
# This file contains the code for plotting the graph using networkx library.
# The code is divided into two parts:
# 1. The first part is for plotting the graph.
# 2. The second part is for plotting the graph features.
##############################################################################

import pandas as pd
from interface import GraphEval, GraphFeatures, TaskGraphFeatures

from .eval_plotter import EvalPlotter as Ep
from .feature_plotter import GraphFeaturesPlotter as Gfp
from .feature_plotter import TaskFeaturesPlotter as Tfp
from .graph_plotter import GraphPlotter as Gp


class PlotGen:
    def __init__(
        self,
        load_graph: pd.DataFrame,
        load_features: pd.DataFrame,
        load_evaluation: pd.DataFrame,
        storage_path: str,
    ):
        self.storage_path = storage_path
        self.graph_list = load_graph
        self.features_list = load_features
        self.evaluation_list = load_evaluation

    def plot_topo(self):
        drawn_topos = set()
        graph_path = f"{self.storage_path}/topo_plot/"
        for index, row in self.graph_list.iterrows():
            graph = row["data"]
            topo = row["topology"]
            if topo not in drawn_topos:
                Gp.plot_graph(graph, graph_path)
                drawn_topos.add(topo)

    def plot_feature(self):
        features_path = f"{self.storage_path}/topo_features_plot/"
        _, row = next(self.features_list.iterrows())
        features = row["feature"]
        if isinstance(features, GraphFeatures):
            Gfp.plot_centrality_features_for_topologies(
                self.features_list, features_path
            )
            Gfp.plot_size_and_centrality_for_topologies(
                self.features_list, features_path
            )
        elif isinstance(features, TaskGraphFeatures):
            Tfp.plot_entropy_and_mutual_information_for_topologies(
                self.features_list, features_path
            )
        else:
            raise ValueError("Invalid features type")

    def plot_eval(self):
        feature_path = f"{self.storage_path}/topo_eval_plot/"
        _, row = next(self.evaluation_list.iterrows())
        evaluation = row["evaluation"]
        if isinstance(evaluation, GraphEval):
            if evaluation.diameter != 0:
                Ep.plot_graph_evaluation(self.evaluation_list, feature_path)
            else:
                Ep.plot_task_graph_evaluation(
                    self.evaluation_list, feature_path
                )
        else:
            raise ValueError("Invalid evaluation type")
