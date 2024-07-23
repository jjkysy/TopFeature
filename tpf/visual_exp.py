import logging

from Plotter.simulation_plotter import plot_hits, plot_max_hits
from Simulator.game_visual import run_simulation

logging.basicConfig(level=logging.INFO)


def main():
    width = 800
    height = 600
    radius = 20
    velocity = 5
    num_agents_list = [15, 30, 150, 300, 900]
    num_steps = 300
    dt = 1
    storage_paths = {
        "simulation_path": "plots/simulation_plots/",
        "animation_save_path": "plots/animation/",
    }
    agent_counts = []
    max_hits_normal_list = []
    max_hits_special_list = []

    for num_agents in num_agents_list:
        (
            cumulative_hits_over_time_normal,
            cumulative_hits_over_time_special,
            max_hits_normal,
            max_hits_special,
        ) = run_simulation(
            width,
            height,
            radius,
            velocity,
            num_agents,
            num_steps,
            dt,
            storage_paths["animation_save_path"]
            + f"simulation_{num_agents}.gif",
        )
        agent_counts.append(num_agents)
        max_hits_normal_list.append(max_hits_normal)
        max_hits_special_list.append(max_hits_special)

        plot_hits(
            num_steps,
            cumulative_hits_over_time_normal,
            cumulative_hits_over_time_special,
            save_path=storage_paths["simulation_path"]
            + f"cumulative_hits_over_time_{num_agents}.png",
        )

    plot_max_hits(
        agent_counts,
        max_hits_normal_list,
        max_hits_special_list,
        save_path=storage_paths["simulation_path"] + "max_hits.png",
    )

    logging.info(f"Agent counts: {agent_counts}")
    logging.info(f"Max hits list (Normal Agents): {max_hits_normal_list}")
    logging.info(f"Max hits list (Special Agents): {max_hits_special_list}")


if __name__ == "__main__":
    main()
