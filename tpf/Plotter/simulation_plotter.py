import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")


def plot_hits(
    num_steps, *cumulative_hits_over_time, save_path, window_size=50
):
    sns.set_theme(style="whitegrid")

    colors = ["b", "g", "r", "c", "m", "y"]
    labels = [
        "No Topology",
        "Batch size a",
        "Batch size b",
        "Batch size c",
        "Batch size d",
        "Batch size e",
    ]

    for hits, color, label in zip(cumulative_hits_over_time, colors, labels):
        hits = np.array(hits)
        smoothed_hits = moving_average(hits, window_size)

        # Here we assume a ±10% range as an example
        # std_deviation = hits * 0.05
        plt.plot(
            # range(num_steps),
            # hits,
            range(len(smoothed_hits)),
            smoothed_hits,
            marker="o",
            markersize=1,
            linestyle="-",
            linewidth=1,
            color=color,
            label=label,
        )

        # # Adding shaded area for the standard deviation
        # plt.fill_between(
        #     range(num_steps),
        #     hits - std_deviation,
        #     hits + std_deviation,
        #     color=color,
        #     alpha=0.2,
        # )

    plt.xlabel("Time Step")
    plt.ylabel("Cumulative Hits")
    plt.title("Cumulative Number of Hits Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    # plt.show()
    plt.close()


def plot_max_hits(agent_counts_list, max_hits_list, save_path):
    """
    param agent_counts_list: list of agent counts
    param max_hits_list: list of tuples of max hits in each group
    param save_path: path to save the plot
    """

    sns.set_theme(style="whitegrid")

    colors = ["b", "g", "r", "c", "m", "y"]
    labels = [
        "No Topology",
        "Batch size a",
        "Batch size b",
        "Batch size c",
        "Batch size d",
        "Batch size e",
    ]

    # range is the length of each tuple in the max_hits_list
    for i in range(len(max_hits_list[0])):
        max_hits_for_group = [hits[i] for hits in max_hits_list]
        plt.plot(
            agent_counts_list,
            max_hits_for_group,
            marker="o",
            linestyle="-",
            color=colors[i],
            label=labels[i],
        )

    plt.xlabel("Number of Agents")
    plt.ylabel("Max Hits by an Agent")
    plt.title("Max Hits by an Agent vs Number of Agents")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    # plt.show()
    plt.close()


def plot_convergence(num_steps, changes_per_step, save_path):
    """
    param num_steps: steps
    param changes_per_step: changes
    param num_agents: agent total count
    param save_path: path to save the plot
    """

    sns.set_theme(style="whitegrid")

    plt.plot(range(num_steps), changes_per_step)
    plt.xlabel("Step")
    plt.ylabel("Change in this step")
    plt.title("Convergence")
    plt.savefig(save_path)
    plt.close()
