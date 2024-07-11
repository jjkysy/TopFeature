import matplotlib.pyplot as plt
import pandas as pd
from utils import PlotStorage as PlotStorage


class GraphFeaturesPlotter:
    average_centrality_mapping = {
        "Avg Degree Centrality": "average_degree_centrality",
        "Avg Betweenness Centrality": "average_betweenness_centrality",
        "Avg Closeness Centrality": "average_closeness_centrality",
        "Avg Second Order Centrality": "average_second_order_centrality",
        "Avg Node Independence": "average_node_independence",
        "Clustering Coefficient": "average_clustering_coefficient",
    }

    @classmethod
    def plot_centrality_features_for_topologies(
        cls, features_frame: pd.DataFrame, storage_path: str
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        for i, centrality_title in enumerate(
            cls.average_centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            for color, (topology_name, features) in zip(
                colors, features_frame.groupby("topology")
            ):
                average_centralities = [
                    feature.__dict__[
                        cls.average_centrality_mapping[centrality_title]
                    ]
                    for feature in features["feature"]
                ]
                plt.scatter(
                    range(100),
                    average_centralities,
                    color=color,
                    label=topology_name,
                )

            plt.title(centrality_title)
            plt.xlabel("Graph")
            plt.ylabel(centrality_title)
            plt.legend()

        plt.tight_layout()
        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot("centrality_comparison")

    @classmethod
    def plot_size_and_centrality_for_topologies(
        cls, features_frame: pd.DataFrame, storage_path: str
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        for i, centrality_title in enumerate(
            cls.average_centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            for color, (topology_name, features) in zip(
                colors, features_frame.groupby("topology")
            ):
                diameters = [
                    feature.diameter for feature in features["feature"]
                ]
                average_centralities = [
                    feature.__dict__[
                        cls.average_centrality_mapping[centrality_title]
                    ]
                    for feature in features["feature"]
                ]
                plt.scatter(
                    diameters,
                    average_centralities,
                    color=color,
                    label=topology_name,
                )

            plt.title(centrality_title)
            plt.xlabel("Diameter")
            plt.ylabel(centrality_title)
            plt.legend()

        plt.tight_layout()
        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot("diameter_centrality")


class TaskFeaturesPlotter:
    @classmethod
    def plot_entropy_and_mutual_information_for_topologies(
        self, features_frame: pd.DataFrame, storage_path: str
    ):
        plt.figure(figsize=(10, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        for i, (topology_name, features) in enumerate(
            features_frame.groupby("topology")
        ):
            entropies = [
                feature.information_entropy for feature in features["feature"]
            ]
            mutual_informations = [
                feature.mutual_information for feature in features["feature"]
            ]
            plt.scatter(
                entropies,
                mutual_informations,
                color=colors[i],
                label=topology_name,
            )

        plt.title("Entropy vs Mutual Information")
        plt.xlabel("Entropy")
        plt.ylabel("Mutual Information")
        plt.legend()
        plt.tight_layout()
        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot("entropy_mutual_information")
