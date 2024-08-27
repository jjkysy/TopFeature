import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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

    # @classmethod
    # def plot_task_graph_evaluation(
    #     cls, evaluation_frame: pd.DataFrame, storage_path: str
    # ):
    #     plt.figure(figsize=(20, 10))
    #     colors = ["b", "g", "r", "c", "m", "y", "k"]
    #     topology_groups = list(evaluation_frame.groupby("topology"))
    #     if len(topology_groups) > len(colors):
    #         raise ValueError(
    #             "Number of topologies exceeds the number of available colors"
    #         )
    #     for i, (topology_name, evaluations) in enumerate(topology_groups):
    #         dependency = [
    #             evaluation.__dict__["dependency"]
    #             for evaluation in evaluations["evaluation"]
    #         ]
    #         uncertainty = [
    #             evaluation.__dict__["uncertainty"]
    #             for evaluation in evaluations["evaluation"]
    #         ]
    #         plt.scatter(
    #             dependency, uncertainty, color=colors[i], label=topology_name
    #         )

    #         z = np.polyfit(dependency, uncertainty, 1)
    #         p = np.poly1d(z)
    #         plt.plot(dependency, p(dependency), color=colors[i])

    #         fit_uncertainty = p(dependency)
    #         std_dev = np.std(uncertainty - fit_uncertainty)
    #         plt.fill_between(
    #             dependency,
    #             fit_uncertainty - std_dev,
    #             fit_uncertainty + std_dev,
    #             color=colors[i],
    #             alpha=0.2,
    #         )

    #     plt.title("Task Graph Evaluation")
    #     plt.xlabel("Dependency")
    #     plt.ylabel("Uncertainty")
    #     plt.legend()
    #     plt.tight_layout()
    #     plot_storage = PlotStorage(storage_path)
    #     plot_storage.save_plot("task_graph_evaluation")

    @classmethod
    def plot_task_graph_evaluation(
        cls, evaluation_frame: pd.DataFrame, storage_path: str
    ):
        plt.figure(figsize=(15, 10))

        # colors = ["blue", "green", "orange", "black",
        #           "cyan", "violet", "red", "magenta"]
        colors = sns.color_palette(
            "colorblind", len(evaluation_frame["topology"].unique())
        )
        topology_groups = list(evaluation_frame.groupby("topology"))

        if len(topology_groups) > len(colors):
            raise ValueError(
                "Number of topologies exceeds the number of available colors"
            )

        # Define the corners of the plot to add as dummy points
        corner_points_dependency = [1.1, 1.45]
        corner_points_uncertainty = [-300, 60]

        hb = None  # Initialize hb to avoid UnboundLocalError

        for i, (topology_name, evaluations) in enumerate(topology_groups):
            dependency = [
                evaluation.__dict__["dependency"]
                for evaluation in evaluations["evaluation"]
            ]
            uncertainty = [
                evaluation.__dict__["uncertainty"]
                for evaluation in evaluations["evaluation"]
            ]

            # Add corner points to the data to ensure consistent plot area
            dependency += corner_points_dependency
            uncertainty += corner_points_uncertainty

            if topology_name.startswith("pruned_"):
                hb = plt.hexbin(
                    dependency,
                    uncertainty,
                    gridsize=40,
                    # cmap="Grays",
                    cmap="viridis",  # Using a colorblind-friendly colormap
                    mincnt=2,
                    alpha=0.6,
                    edgecolors=colors[i],  # Using edge color to distinguish
                    # edgecolors='none'
                )
                # Mark the first point with a special marker
                plt.scatter(
                    dependency[0],
                    uncertainty[0],
                    color=colors[i],
                    s=100,
                    edgecolor="white",
                    zorder=5,
                    label=f"{topology_name} Starting",
                )
            else:
                # Plot scatter for non-pruned topologies
                # plt.scatter(
                #     dependency, uncertainty,
                #     color=colors[i], s=100, edgecolor='white',
                #     zorder=5, label=f'{topology_name}'
                # )
                # Plot KDE for non-pruned topologies
                sns.kdeplot(
                    x=dependency,
                    y=uncertainty,
                    fill=True,
                    color=colors[i],
                    alpha=0.5,
                    label=f"{topology_name}",
                )

        if hb is not None:
            cbar = plt.colorbar(hb)
            cbar.set_label("Count in Bin", fontsize=24)
            cbar.ax.tick_params(labelsize=16)
        plt.title("Graph Evaluation: Dependency vs. Uncertainty", fontsize=26)
        plt.xlabel("Dependency", fontsize=24)
        plt.ylabel("Uncertainty", fontsize=24)
        plt.xticks(fontsize=16)  # Increase x-axis ticks label size
        plt.yticks(fontsize=16)  # Increase y-axis ticks label size
        plt.legend(loc="lower left", fontsize=20)
        plt.grid(
            True, linestyle="--", alpha=0.5
        )  # Add a grid for better readability
        plt.tight_layout()

        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot("task_graph_evaluation_hexbin")
