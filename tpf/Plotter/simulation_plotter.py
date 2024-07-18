import matplotlib.pyplot as plt


def plot_hits(
    num_steps,
    cumulative_hits_over_time,
    special_cumulative_hits_over_time,
    save_path,
):
    plt.plot(
        range(num_steps),
        cumulative_hits_over_time,
        marker="o",
        linestyle="-",
        color="b",
        label="Normal Agents",
    )
    plt.plot(
        range(num_steps),
        special_cumulative_hits_over_time,
        marker="o",
        linestyle="-",
        color="r",
        label="Special Agent",
    )
    plt.xlabel("Time Step")
    plt.ylabel("Cumulative Hits")
    plt.title("Cumulative Number of Hits Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    plt.show()
