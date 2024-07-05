##############################################################################
# This file contains the code for plotting the graph using networkx library.
# The code is divided into two parts:
# 1. The first part is for plotting the graph.
# 2. The second part is for plotting the graph features.
##############################################################################

from typing import Dict, List
import networkx as nx
import matplotlib.pyplot as plt
import os
from interface import GraphData, GraphFeatures


# The first part
class GraphPlotter:
    @classmethod
    def plot_graph(cls, graph: nx.DiGraph, name: str, path: str):
        # if name == "chain_xxx": use circular layout
        # else: use spring layout
        if "chain" in name:
            plt.figure(figsize=(10, 10))
            pos = nx.circular_layout(graph)
        else:
            plt.figure(figsize=(10, 10))
            pos = nx.spring_layout(graph)
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_size=100,
            node_color="skyblue",
            font_size=8,
        )
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
    centrality_mapping = {
        "Average Degree Centrality": "degree_centrality",
        "Average Betweenness Centrality": "betweenness_centrality",
        "Average Closeness Centrality": "closeness_centrality",
        # "Average Edge Betweenness Centrality": "edge_betweenness_centrality",
        "Average Second Order Centrality": "second_order_centrality",
        "Average Node Independence": "node_independence",
        "Clustering Coefficient": "clustering_coefficient",
    }

    @classmethod
    def plot_centrality_features(cls, feature: GraphFeatures, path: str):
        plt.figure(figsize=(12, 4))
        centrality_measures = [
            ("Degree Centrality", feature.degree_centrality),
            ("Betweenness Centrality", feature.betweenness_centrality),
            ("Closeness Centrality", feature.closeness_centrality),
            ("Second Order Centrality", feature.second_order_centrality),
        ]

        for i, (title, centrality) in enumerate(centrality_measures, start=1):
            plt.subplot(2, 3, i)
            plt.scatter(list(centrality.keys()), list(centrality.values()))
            plt.title(title)
            plt.xlabel("Node")
            plt.ylabel(title)

        plt.tight_layout()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(f"{path}{feature.name}_centrality.png")
        plt.close()

    @classmethod
    def plot_features_within_one_graph(
        cls, features: List[GraphFeatures], path: str
    ):
        for feature_set in features[:1]:
            cls.plot_centrality_features(feature_set, path)

    @classmethod
    def plot_size_features_for_topologies(
        cls, features: List[GraphFeatures], path: str
    ):
        name = features[0].name
        diameter = []
        for feature in features[0:100]:
            diameter.append(feature.diameter)
        plt.scatter(range(100), diameter)
        plt.title(f"Diameter of {name}")
        plt.xlabel("Graph")
        plt.ylabel("Diameter")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(f"{path}{name}_diameter.png")
        plt.close()

    @classmethod
    def plot_centrality_features_for_topologies(
        cls, features_dict: Dict[str, List[GraphFeatures]], path: str
    ):
        """
        :param features_dict: a dictionary, the key is the topology name,
            the value is the list of GraphFeatures.
        :param path: the path to save the plots.
        """
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]

        def calculate_average_centrality(feature_set, centrality_type):
            return sum(getattr(feature_set, centrality_type).values()) / len(
                getattr(feature_set, centrality_type)
            )

        for i, centrality_title in enumerate(
            cls.centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            for color, (topology_name, features) in zip(
                colors, features_dict.items()
            ):
                average_centralities = [
                    calculate_average_centrality(
                        feature_set,
                        cls.centrality_mapping[centrality_title],
                    )
                    for feature_set in features
                ]
                graph_numbers = list(range(1, len(features) + 1))
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
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(f"{path}average_centrality_comparison.png")
        plt.close()

        # draw another plot with boxplot
        plt.figure(figsize=(20, 10))
        for i, centrality_title in enumerate(
            cls.centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            data = [
                [
                    calculate_average_centrality(
                        feature_set,
                        cls.centrality_mapping[centrality_title],
                    )
                    for feature_set in features
                ]
                for features in features_dict.values()
            ]
            plt.boxplot(data, labels=features_dict.keys())
            plt.title(centrality_title)
            plt.ylabel("Average Centrality")

        plt.tight_layout()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(f"{path}average_centrality_boxplot.png")
        plt.close()

    @classmethod
    def plot_size_and_centrality_for_topologies(
        cls, features_dict: Dict[str, List[GraphFeatures]], path: str
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]

        def calculate_average_centrality(feature_set, centrality_type):
            return sum(getattr(feature_set, centrality_type).values()) / len(
                getattr(feature_set, centrality_type)
            )

        for i, centrality_title in enumerate(
            cls.centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            for color, (topology_name, features) in zip(
                colors, features_dict.items()
            ):
                average_centralities = [
                    calculate_average_centrality(
                        feature_set,
                        cls.centrality_mapping[centrality_title],
                    )
                    for feature_set in features
                ]
                diameters = [feature.diameter for feature in features]
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
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(f"{path}diameter_centrality.png")
        plt.close()
