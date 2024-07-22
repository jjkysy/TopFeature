import concurrent.futures

from Env_simulator.game import run_simulation
from Plotter.simulation_plotter import plot_hits, plot_max_hits


def run_simulation_for_agents(
    num_agents, width, height, radius, velocity, num_steps, dt
):
    return run_simulation(
        width, height, radius, velocity, num_agents, num_steps, dt
    )


def main():
    width = 800
    height = 600
    radius = 20
    velocity = 5
    num_agents_list = [15, 30, 150, 300, 900, 1500]
    num_steps = 100
    dt = 1
    storage_paths = {
        "simulation_path": "plots/simulation_plots/",
        # add ...
    }
    agent_counts = []
    max_hits_normal_list = []
    max_hits_special_list = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                run_simulation_for_agents,
                num_agents,
                width,
                height,
                radius,
                velocity,
                num_steps,
                dt,
            )
            for num_agents in num_agents_list
        ]

        for future, num_agents in zip(
            concurrent.futures.as_completed(futures), num_agents_list
        ):
            (
                cumulative_hits_over_time_normal,
                cumulative_hits_over_time_special,
                max_hits_normal,
                max_hits_special,
            ) = future.result()
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

    print(f"Agent counts: {agent_counts}")
    print(f"Max hits list (Normal Agents): {max_hits_normal_list}")
    print(f"Max hits list (Special Agents): {max_hits_special_list}")


if __name__ == "__main__":
    main()
