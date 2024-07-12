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
    def _plot_features(
        cls, features_frame, storage_path, plot_name, x_label, x_attr=None
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        topology_groups = list(features_frame.groupby("topology"))

        if len(topology_groups) > len(colors):
            raise ValueError(
                "Number of topologies exceeds the number of available colors"
            )

        for i, centrality_title in enumerate(
            cls.average_centrality_mapping.keys(), start=1
        ):
            plt.subplot(2, 3, i)
            for color, (topology_name, features) in zip(
                colors, topology_groups
            ):
                x_values = [
                    feature.__dict__[x_attr] if x_attr else index
                    for index, feature in enumerate(features["feature"])
                ]
                y_values = [
                    feature.__dict__[
                        cls.average_centrality_mapping[centrality_title]
                    ]
                    for feature in features["feature"]
                ]

                plt.scatter(
                    x_values, y_values, color=color, label=topology_name
                )

            plt.title(centrality_title)
            plt.xlabel(x_label)
            plt.ylabel(centrality_title)
            plt.legend()

        plt.tight_layout()
        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot(plot_name)

    @classmethod
    def plot_centrality_features_for_topologies(
        cls, features_frame: pd.DataFrame, storage_path: str
    ):
        cls._plot_features(
            features_frame, storage_path, "centrality_comparison", "Graph"
        )

    @classmethod
    def plot_size_and_centrality_for_topologies(
        cls, features_frame: pd.DataFrame, storage_path: str
    ):
        cls._plot_features(
            features_frame,
            storage_path,
            "diameter_centrality",
            "Diameter",
            x_attr="diameter",
        )


class TaskFeaturesPlotter:
    @classmethod
    def plot_entropy_and_mutual_information_for_topologies(
        cls, features_frame: pd.DataFrame, storage_path: str
    ):
        plt.figure(figsize=(10, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        topology_groups = list(features_frame.groupby("topology"))
        if len(topology_groups) > len(colors):
            raise ValueError(
                "Number of topologies exceeds the number of available colors"
            )
        for i, (topology_name, features) in enumerate(topology_groups):
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
