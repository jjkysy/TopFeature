#################################################################################
# This file contains the code for plotting the graph using networkx library.
# The code is divided into two parts:
# 1. The first part is for plotting the graph.
# 2. The second part is for plotting the graph features.

# class GraphFeatures:
    # name: str
    # degree_centrality: Dict[Any, float] = field(default_factory=dict)
    # betweenness_centrality: Dict[Any, float] = field(default_factory=dict)
    # closeness_centrality: Dict[Any, float] = field(default_factory=dict)
    # edge_betweenness_centrality: Dict[Any, float] = field(default_factory=dict)
    # eccentricity: Dict[Any, int] = field(default_factory=dict)
    # diameter: int = 0
    # radius: int = 0
    # node_independence: Dict[Any, float] = field(default_factory=dict)
    # second_order_centrality: Dict[Any, float] = field(default_factory=dict)
    # clustering_coefficient: Dict[Any, float] = field(default_factory=dict)    
#################################################################################

from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import os

from interface import GraphData, GraphFeatures

# The first part
class GraphPlotter:
    @classmethod
    def plot_graph(cls, graph: nx.DiGraph, name: str, path: str):
        plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=100, node_color="skyblue")
        plt.title(name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(f"{path}{name}.png")
        plt.close()

    @classmethod
    def plot_graphs(cls, graphs: List[GraphData], path: str):
        # only plot the first graph for now (100 in total)
        for graph_data in graphs[:1]:
            cls.plot_graph(graph_data.graph, graph_data.name, path)

# The second part, plotting the graph features with scatter plots
class GraphFeaturesPlotter:
    @classmethod
    def plot_centrality_features(cls, feature: GraphFeatures, path: str):
        plt.figure(figsize=(12, 4))
        centrality_measures = [
            ("Degree Centrality", feature.degree_centrality),
            ("Betweenness Centrality", feature.betweenness_centrality),
            ("Closeness Centrality", feature.closeness_centrality),
        ]

        for i, (title, centrality) in enumerate(centrality_measures, start=1):
            plt.subplot(1, 3, i)
            plt.scatter(list(centrality.keys()), list(centrality.values()))
            plt.title(title)
            plt.xlabel("Node")
            plt.ylabel(title)

        plt.tight_layout()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(f"{path}{feature.name}_centrality.png")
        plt.close()

    # TODO: add more plots for other features

    @classmethod
    def plot_features(cls, features: List[GraphFeatures], path: str):
        for feature_set in features[:1]:
            cls.plot_centrality_features(feature_set, path)