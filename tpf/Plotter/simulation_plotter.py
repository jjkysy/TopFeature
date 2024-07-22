import matplotlib.pyplot as plt


def plot_hits(
    num_steps, cumulative_hits_normal, cumulative_hits_special, save_path
):
    plt.plot(
        range(num_steps),
        cumulative_hits_normal,
        marker="o",
        linestyle="-",
        color="b",
        label="Normal Agents",
    )
    plt.plot(
        range(num_steps),
        cumulative_hits_special,
        marker="o",
        linestyle="-",
        color="r",
        label="Special Agents",
    )
    plt.xlabel("Time Step")
    plt.ylabel("Cumulative Hits")
    plt.title("Cumulative Number of Hits Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    # plt.show()
    plt.close()


def plot_max_hits(
    agent_counts, max_hits_normal_list, max_hits_special_list, save_path
):
    plt.plot(
        agent_counts,
        max_hits_normal_list,
        marker="o",
        linestyle="-",
        color="b",
        label="Normal Agents",
    )
    plt.plot(
        agent_counts,
        max_hits_special_list,
        marker="o",
        linestyle="-",
        color="r",
        label="Special Agents",
    )
    plt.xlabel("Number of Agents")
    plt.ylabel("Max Hits by an Agent")
    plt.title("Max Hits by an Agent vs Number of Agents")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    # plt.show()
