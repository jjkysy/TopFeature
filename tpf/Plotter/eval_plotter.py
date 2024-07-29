import matplotlib.pyplot as plt
import pandas as pd
from utils import PlotStorage as PlotStorage


class EvalPlotter:

    @classmethod
    def plot_graph_evaluation(
        cls, evaluation_frame: pd.DataFrame, storage_path: str
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        topology_groups = list(evaluation_frame.groupby("topology"))
        if len(topology_groups) > len(colors):
            raise ValueError(
                "Number of topologies exceeds the number of available colors"
            )
        for i, evaluation_title in enumerate(["dependency", "uncertainty"]):
            plt.subplot(1, 2, i + 1)
            for color, (topology_name, evaluations) in zip(
                colors, topology_groups
            ):
                x_values = [
                    evaluation.__dict__["diameter"]
                    for evaluation in evaluations["evaluation"]
                ]
                y_values = [
                    evaluation.__dict__[evaluation_title]
                    for evaluation in evaluations["evaluation"]
                ]
                plt.scatter(
                    x_values, y_values, color=color, label=topology_name
                )

            plt.title(evaluation_title)
            plt.xlabel("Diameter")
            plt.ylabel(evaluation_title)
            plt.legend()

        plt.tight_layout()
        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot("graph_evaluation")

    @classmethod
    def plot_task_graph_evaluation(
        cls, evaluation_frame: pd.DataFrame, storage_path: str
    ):
        plt.figure(figsize=(20, 10))
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        topology_groups = list(evaluation_frame.groupby("topology"))
        if len(topology_groups) > len(colors):
            raise ValueError(
                "Number of topologies exceeds the number of available colors"
            )
        for i, (topology_name, evaluations) in enumerate(topology_groups):
            dependency = [
                evaluation.__dict__["dependency"]
                for evaluation in evaluations["evaluation"]
            ]
            uncertainty = [
                evaluation.__dict__["uncertainty"]
                for evaluation in evaluations["evaluation"]
            ]
            plt.scatter(
                dependency, uncertainty, color=colors[i], label=topology_name
            )
        plt.title("Task Graph Evaluation")
        plt.xlabel("Dependency")
        plt.ylabel("Uncertainty")
        plt.legend()
        plt.tight_layout()
        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot("task_graph_evaluation")
