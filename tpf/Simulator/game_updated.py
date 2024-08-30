# use pruned adjacency matrix to simulate the needle throwing game
# can refer to game.py
# only difference is omega will not change

import logging
from typing import List, Tuple

import numpy as np
from Agent_simulator.agent import _Agent  # Agent
from Agent_simulator.update_strategy import Para_update_strategies as Opinion
from Env_simulator.env import Env

# from Plotter.simulation_plotter import plot_convergence
from shapely.geometry import Point
from utils import calculate_hits

logging.basicConfig(level=logging.INFO)

save_path_dict = {
    "simulation": "plots/simulation_plots/",
    "task_matrix": "stats/task_matrix/",
    "pruned_matrix": "stats/pruned_matrix/",
    "hits": "stats/hits/",
}

omega_matrix = np.load(save_path_dict["pruned_matrix"] + "pruned_50.npy")


def update_agents(
    agents: List[_Agent],
    len_agents: int,
    omega_matrix: np.ndarray,
) -> Tuple[float, np.ndarray]:
    for agent in agents:
        Opinion.FJ_update_parameters_adapt(
            agent, len_agents, omega_matrix, agents
        )

    return 0.0, np.zeros((len_agents, len_agents))


def run_simulation(
    width,
    height,
    radius,
    initial_boundary_width,
    velocity,
    num_agents,
    dt,
    num_steps,
    expansion_times,
    link_percentage_list,
):
    # create environment
    env = Env(
        width,
        height,
        radius,
        velocity,
        initial_boundary_width,
        expansion_times,
        rdn_seed=42,
    )

    training_group_number = len(link_percentage_list)
    total_group_number = training_group_number + 1

    def create_adjcacency_matrix(
        num_agents, link_percentage_list
    ) -> list[np.array]:
        # create a adjcency matrix to represent a mesh topology
        matrix_to_return = []
        for link_percentage in link_percentage_list:
            mesh_adjacency_matrix = (
                np.random.rand(num_agents, num_agents) < link_percentage
            ).astype(int)
            np.fill_diagonal(mesh_adjacency_matrix, 0)
            matrix_to_return.append(mesh_adjacency_matrix)

        return matrix_to_return

    # initialize variables
    cumulative_hits_over_time = [[] for _ in range(total_group_number)]
    agent_hits = [[0] * num_agents for _ in range(total_group_number)]
    total_hits = [0] * total_group_number

    omega_matrices = [
        np.load(save_path_dict["pruned_matrix"] + f"pruned_{num_agents}.npy")
        for _ in range(training_group_number)
    ]

    expansion_factor = expansion_times ** (1 / num_steps)

    # create agents: groups of dynamic agents and 1 group of static agents
    dynamic_agents = [
        _Agent.create(i, env.get_boundary())
        for i in range(num_agents * training_group_number)
    ]
    static_agents = [
        _Agent.create(
            i + training_group_number * num_agents, env.get_boundary()
        )
        for i in range(num_agents)
    ]
    all_agents = dynamic_agents + static_agents

    # start simulation
    for step in range(num_steps):
        # expand polygon and move the agents
        env.expand_boundary(expansion_factor)
        for agent in all_agents:
            _Agent.update_boundary(agent, env.get_boundary())
        hits_info = [{} for _ in range(training_group_number)]
        for agent in all_agents:
            _Agent.move(agent, dt)

        # five group of dynamic agents
        dynamic_agents_groups = [
            dynamic_agents[slice(i * num_agents, (i + 1) * num_agents)]
            for i in range(training_group_number)
        ]

        # calculate hits
        hits = [calculate_hits(static_agents, env.get_target_hole())] + [
            calculate_hits(group, env.get_target_hole())
            for group in dynamic_agents_groups
        ]

        # update cumulative hits info
        for i, hit_group in enumerate(hits):
            for hit in hit_group:
                idx = hit.id % num_agents
                agent_hits[i][idx] += 1
                if i > 0:
                    hits_info[i - 1][
                        dynamic_agents_groups[i - 1][idx].id
                    ] = hit
            total_hits[i] += len(hit_group)
            cumulative_hits_over_time[i].append(total_hits[i])

        # move the hole
        old_position = Point(env.hole_x, env.hole_y)
        new_position = env.move_hole(dt)
        env.update_state_transition_matrix(
            old_position.x, old_position.y, new_position.x, new_position.y
        )

        for i, group in enumerate(dynamic_agents_groups):
            update_agents(
                group,
                num_agents,
                omega_matrices[i],
            )

        # print(omega_matrices[-1])

    # save task matrix and check its properties
    # now, no need to save but only check if it is same with the previous one
    task_matrix = env.state_transition_matrix
    assert not np.all(task_matrix == 0)
    for row in task_matrix:
        assert np.sum(row) == 1 or np.sum(row) == 0

    previous_task_matrix = np.load(
        save_path_dict["task_matrix"] + str(num_agents) + ".npy"
    )
    assert np.all(task_matrix == previous_task_matrix)

    logging.info("Task matrix same as previous one")

    # also save the cumulative_hits_over_time
    np.save(
        save_path_dict["hits"]
        + f"optimized_cumulative_hits_over_time_{num_agents}.npy",
        cumulative_hits_over_time,
    )
    logging.info(
        f"Cumulative hits over time saved at {save_path_dict['hits']}"
        f"optimized_cumulative_hits_over_time_{num_agents}.npy"
    )

    # return cumulative hits over time and max hits
    max_hits = [max(hits) for hits in agent_hits]
    return (
        *cumulative_hits_over_time,
        *max_hits,
    )
