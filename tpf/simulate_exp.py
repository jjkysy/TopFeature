import concurrent.futures
import logging

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
    "num_steps": 1000,
    "expansion_times": 3,
}


num_agents_list = [10, 20, 30, 50, 100, 200, 300, 400]


def run_simulation_for_agents(**params):
    return run_simulation(**params)


# def main():

#     agent_counts = []
#     max_hits_normal_list = []
#     max_hits_special_list = []

#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         futures = [
#             executor.submit(
#                 run_simulation_for_agents, num_agents=num, **params
#             )
#             for num in num_agents_list
#         ]

#         for future, num_agents in zip(
#             concurrent.futures.as_completed(futures), num_agents_list
#         ):
#             (
#                 *cumulative_hits_over_time,
#                 *max_hits,
#             ) = future.result()
#             agent_counts.append(num_agents)

#             plot_hits(
#                 params["num_steps"],
#                 *cumulative_hits_over_time,
#                 save_path="plots/simulation_plots/"
#                 + f"cumulative_hits_over_time_{num_agents}.png",
#             )

#     plot_max_hits(
#         agent_counts,
#         *max_hits,
#         save_path="plots/simulation_plots/" + "max_hits.png",
#     )

#     logging.info(f"Agent counts: {agent_counts}")
#     logging.info(f"Max hits list (Normal Agents): {max_hits_normal_list}")
#     logging.info(f"Max hits list (Special Agents): {max_hits_special_list}")


def main():
    agent_counts = []
    max_hits_normal_list = []
    max_hits_special_list = []

    for num_agents in num_agents_list:
        result = run_simulation_for_agents(num_agents=num_agents, **params)
        cumulative_hits_over_time = result[:-2]
        max_hits = result[-2:]
        agent_counts.append(num_agents)

        plot_hits(
            params["num_steps"],
            *cumulative_hits_over_time,
            save_path="plots/simulation_plots/"
            + f"cumulative_hits_over_time_{num_agents}.png",
        )

    plot_max_hits(
        agent_counts,
        *max_hits,
        save_path="plots/simulation_plots/" + "max_hits.png",
    )

if __name__ == "__main__":
    main()
