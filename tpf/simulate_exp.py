import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

from Plotter.simulation_plotter import plot_hits, plot_max_hits
from Simulator.game import run_simulation

logging.basicConfig(level=logging.INFO)

params = {
    "width": 80,
    "height": 60,
    "radius": 2,
    "initial_boundary_width": 10,
    "velocity": 1,
    "dt": 1,
    "num_steps": 2000,
    "expansion_times": 5,
}

num_agents_list = [10, 20, 30, 50, 80]
# [200, 300]
# [10, 20, 30, 50, 80, 100]


def run_simulation_for_agents(num_agents, **params):
    return run_simulation(num_agents=num_agents, **params)


def main():
    agent_counts_list = []
    max_hits_list = []

    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(
                run_simulation_for_agents, num_agents, **params
            ): num_agents
            for num_agents in num_agents_list
        }

        for future in as_completed(futures):
            num_agents = futures[future]
            try:
                result = future.result()
                cumulative_hits_over_time = result[slice(0, len(result) // 2)]
                max_hits = result[slice(len(result) // 2, len(result))]
                agent_counts_list.append(num_agents)
                max_hits_list.append(max_hits)

                plot_hits(
                    params["num_steps"],
                    *cumulative_hits_over_time,
                    save_path=(
                        f"plots/simulation_plots/"
                        f"cumulative_hits_over_time_{num_agents}.png"
                    ),
                )
            except Exception as exc:
                logging.error(
                    f"Simulation for {num_agents} agents"
                    f"generated an exception: {exc}"
                )

    plot_max_hits(
        agent_counts_list,
        max_hits_list,
        save_path="plots/simulation_plots/max_hits.png",
    )


if __name__ == "__main__":
    main()
