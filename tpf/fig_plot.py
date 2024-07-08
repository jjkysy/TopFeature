##############################################################################
# This file contains the code for plotting the graph using networkx library.
# The code is divided into two parts:
# 1. The first part is for plotting the graph.
# 2. The second part is for plotting the graph features.
##############################################################################

from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tpf.interface import GraphData, GraphFeatures


class PlotStorage:
    def __init__(self, path: str):
        sns.set_theme(style="whitegrid")
        # TODO: adjust the sns style
        self.path = path

    def save_plot(self, name: str):
        full_path = os.path.join(self.path, f"{name}.png")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        plt.savefig(full_path)
        plt.close()


class GraphPlotter:
    def __init__(self, path: str):
        self.plot_storage = PlotStorage(path)
        self.layout_mapping = {
            "chain_0": nx.circular_layout,
            "mesh_0": nx.spring_layout,
            "pool_0": nx.spring_layout,
            "star_0": nx.spring_layout,
            "hierarchical_0": nx.spring_layout,
        }

    def plot_graph(self, graph: nx.DiGraph, name: str):
        plt.figure(figsize=(10, 10))
        layout_func = self.layout_mapping.get(name, nx.spring_layout)
        pos = layout_func(graph)
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_size=100,
            node_color="skyblue",
            font_size=8,
        )
        plt.title(name)
        self.plot_storage.save_plot(name)

    def plot_graphs(self, graphs: List[GraphData]):
        # only plot the first graph for now (100 in total)
        for graph_data in graphs[:1]:
            self.plot_graph(graph_data.graph, graph_data.name)


class GraphFeaturesPlotter:
    def __init__(self, path: str):
        self.plot_storage = PlotStorage(path)

    def plot_centrality_features(self, feature: GraphFeatures):
        plt.figure(figsize=(12, 4))
        centrality_measures = [
            ("Degree Centrality", feature.degree_centrality),
            (
                "Betweenness Centrality",
                feature.betweenness_centrality,
            ),
            ("Closeness Centrality", feature.closeness_centrality),
            (
                "Second Order Centrality",
                feature.second_order_centrality,
            ),
        ]

        for i, (title, centrality) in enumerate(centrality_measures, start=1):
            plt.subplot(2, 3, i)
            plt.scatter(list(centrality.keys()), list(centrality.values()))
            plt.title(title)
            plt.xlabel("Node")
            plt.ylabel(title)

        plt.tight_layout()
        self.plot_storage.save_plot(f"{feature.name}_centrality")

    def plot_features_within_one_graph(self, features: List[GraphFeatures]):
        for feature_set in features[:1]:
            self.plot_centrality_features(feature_set)


class TopoFeaturesPlotter:
    def __init__(self, path: str):
        self.plot_storage = PlotStorage(path)
        self.path = path
        self.average_centrality_mapping = {
            "Avg Degree Centrality": "average_degree_centrality",
            "Avg Betweenness Centrality": "average_betweenness_centrality",
            "Avg Closeness Centrality": "average_closeness_centrality",
            "Avg Second Order Centrality": "average_second_order_centrality",
            "Avg Node Independence": "average_node_independence",
            "Clustering Coefficient": "average_clustering_coefficient",
        }

    def plot_size_features_for_topologies(self, features: List[GraphFeatures]):
        name = features[0].name
        diameter = []
        for feature in features[0:100]:
            diameter.append(feature.diameter)
        plt.scatter(range(len(diameter)), diameter)
        plt.title(f"Diameter of {name}")
        plt.xlabel("Graph")
        plt.ylabel("Diameter")
        self.plot_storage.save_plot(f"{name}_diameter")

    def plot_centrality_features_for_topologies(
        self, features_dict: Dict[str, List[GraphFeatures]]
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        for i, centrality_title in enumerate(
            self.average_centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            for color, (topology_name, features) in zip(
                colors, features_dict.items()
            ):
                graph_numbers = list(range(1, len(features) + 1))
                average_centralities = [
                    feature.__dict__[
                        self.average_centrality_mapping[centrality_title]
                    ]
                    for feature in features
                ]
                plt.scatter(
                    graph_numbers,
                    average_centralities,
                    color=color,
                    label=topology_name,
                )

            plt.title(centrality_title)
            plt.xlabel("Graph ID")
            plt.ylabel("Average Centrality")
            plt.legend()

        plt.tight_layout()
        self.plot_storage.save_plot("average_centrality_comparison")

    def plot_size_and_centrality_for_topologies(
        self, features_dict: Dict[str, List[GraphFeatures]]
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        for i, centrality_title in enumerate(
            self.average_centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            for color, (topology_name, features) in zip(
                colors, features_dict.items()
            ):
                diameters = [feature.diameter for feature in features]
                average_centralities = [
                    feature.__dict__[
                        self.average_centrality_mapping[centrality_title]
                    ]
                    for feature in features
                ]
                plt.scatter(
                    diameters,
                    average_centralities,
                    color=color,
                    label=topology_name,
                )

            plt.title(centrality_title)
            plt.xlabel("Diameter")
            plt.ylabel("Average Centrality")
            plt.legend()

        plt.tight_layout()
        self.plot_storage.save_plot("diameter_centrality")
