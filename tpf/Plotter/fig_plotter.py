##############################################################################
# This file contains the code for plotting the graph using networkx library.
# The code is divided into two parts:
# 1. The first part is for plotting the graph.
# 2. The second part is for plotting the graph features.
##############################################################################

import pandas as pd
from .graph_plotter import GraphPlotter as Gp
from .feature_plotter import (
    GraphFeaturesPlotter as Gfp,
    TaskFeaturesPlotter as Tfp,
)
from interface import GraphFeatures, TaskGraphFeatures


class PlotGen:
    def __init__(
        self,
        load_graph: pd.DataFrame,
        load_features: pd.DataFrame,
        storage_path: str,
    ):
        self.storage_path = storage_path
        self.graph_list = load_graph
        self.features_list = load_features

    def graph_plot(self):
        drawn_topos = set()
        graph_path = self.storage_path + "topo_plot/"
        for index, row in self.graph_list.iterrows():
            graph = row["data"]
            topo = row["topology"]
            if topo not in drawn_topos:
                Gp.plot_graph(graph, graph_path)
                drawn_topos.add(topo)

    def feature_plot(self):
        drawn_topos = set()
        features_path = self.storage_path + "topo_features_plot/"
        for index, row in self.features_list.iterrows():
            features = row["feature"]
            topo = row["topology"]
            if topo not in drawn_topos:
                drawn_topos.add(topo)
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
