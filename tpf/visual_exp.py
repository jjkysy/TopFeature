import logging

from Plotter.simulation_plotter import plot_hits, plot_max_hits
from Simulator.game_visual import run_simulation

logging.basicConfig(level=logging.INFO)


params = {
    "width": 80,
    "height": 60,
    "radius": 2,
    "initial_boundary_width": 10,
    "velocity": 1,
    "dt": 1,
    "num_steps": 2000,
    "FPS": 20,
    "expansion_times": 3,
}


num_agents_list = [10, 20, 30, 50, 100, 200, 300, 400]


def run_simulation_for_agents(**params):
    return run_simulation(**params)


def main():
    agent_counts_list = []
    max_hits_list = []

    for num_agents in num_agents_list:
        result = run_simulation_for_agents(num_agents=num_agents, **params)
        cumulative_hits_over_time = result[slice(0, len(result) // 2)]
        max_hits = result[slice(len(result) // 2, len(result))]
        agent_counts_list.append(num_agents)
        max_hits_list.append(max_hits)

        plot_hits(
            params["num_steps"],
            *cumulative_hits_over_time,
            save_path="plots/simulation_plots/"
            + f"cumulative_hits_over_time_{num_agents}.png",
        )

    plot_max_hits(
        agent_counts_list,
        max_hits_list,
        save_path="plots/simulation_plots/" + "max_hits.png",
    )


if __name__ == "__main__":
    main()
