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
    "num_agents": 50,
    "dt": 1,
    "num_steps": 2000,
    "FPS": 20,
    "expansion_times": 3,
    # "learning_rate": 0.01,
    # "theta": 10,
    # "gamma": 0.9,
    # "epsilon": 0.5,
    # "batch_size": 64,
    # "q_network_params": {"input_dim": 2, "output_dim": 360},
}


num_agents_list = [10, 20, 50, 100, 200, 500]

storage_paths = {
    "simulation_path": "plots/simulation_plots/",
    "animation_save_path": "plots/animation/",
}


def main():

    agent_counts = []
    max_hits_normal_list = []
    max_hits_special_list = []

    for num_agents in num_agents_list:
        params["num_agents"] = num_agents
        (
            cumulative_hits_over_time_normal,
            cumulative_hits_over_time_special,
            max_hits_normal,
            max_hits_special,
        ) = run_simulation(**params)
        agent_counts.append(num_agents)
        max_hits_normal_list.append(max_hits_normal)
        max_hits_special_list.append(max_hits_special)

        plot_hits(
            params["num_steps"],
            cumulative_hits_over_time_normal,
            cumulative_hits_over_time_special,
            save_path="plots/simulation_plots/"
            + f"cumulative_hits_over_time_{num_agents}.png",
        )

    plot_max_hits(
        agent_counts,
        max_hits_normal_list,
        max_hits_special_list,
        save_path="plots/simulation_plots/" + "max_hits.png",
    )

    logging.info(f"Agent counts: {agent_counts}")
    logging.info(f"Max hits list (Normal Agents): {max_hits_normal_list}")
    logging.info(f"Max hits list (Special Agents): {max_hits_special_list}")


if __name__ == "__main__":
    main()
