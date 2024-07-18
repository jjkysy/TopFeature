from Env_simulator.game_visual import run_simulation
from Plotter.simulation_plotter import plot_hits


def simulation_loop():
    width = 800
    height = 600
    radius = 20
    velocity = 5
    num_agents = 100
    num_steps = 100
    dt = 1
    storage_paths = {
        "simulation_path": "plots/simulation_plots/",
        # add ...
    }
    cumulative_hits_over_time, special_cumulative_hits_over_time = (
        run_simulation(
            width, height, radius, velocity, num_agents, num_steps, dt
        )
    )

    plot_hits(
        num_steps,
        cumulative_hits_over_time,
        special_cumulative_hits_over_time,
        storage_paths["simulation_path"],
    )


if __name__ == "__main__":
    simulation_loop()
