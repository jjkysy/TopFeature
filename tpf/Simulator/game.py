import logging
from typing import List, Tuple

import numpy as np
from Agent_simulator.agent import _Agent  # Agent
from Agent_simulator.update_strategy import Para_update_strategies as Opinion
from Env_simulator.env import Env
from Plotter.simulation_plotter import plot_convergence
from shapely.geometry import Point
from utils import calculate_hits

logging.basicConfig(level=logging.INFO)

save_path_dict = {
    "simulation": "plots/simulation_plots/",
    "task_matrix": "plots/task_matrix/",
}


def update_agents(
    agents: List[_Agent],
    len_agents: int,
    omega_matrix: np.ndarray,
    hits_info: List[dict],
    temp_matrix: np.ndarray,
) -> Tuple[float, np.ndarray]:
    for agent in agents:
        # Opinion.FJ_update_parameters_adapt(
        #     agent, len_agents, omega_matrix, agents, temp_matrix
        # )
        Opinion.FJ_update_parameters(
            agent, len_agents, omega_matrix, agents, temp_matrix
        )
    change_in_this_step, omega_matrix = _Agent.update_omega_matrix(
        omega_matrix, hits_info
    )
    return change_in_this_step, omega_matrix


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
):
    # create environment
    env = Env(
        width,
        height,
        radius,
        velocity,
        initial_boundary_width,
        expansion_times,
    )

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

        # create a adjcency matrix to represent a star topology
        star_adjacency_matrix = np.zeros((num_agents, num_agents))
        star_adjacency_matrix[:, 0] = 1
        star_adjacency_matrix[0, :] = 1
        np.fill_diagonal(star_adjacency_matrix, 0)
        matrix_to_return.append(star_adjacency_matrix)

        # create a adjcency matrix to represent a ring topology
        ring_adjacency_matrix = np.zeros((num_agents, num_agents))
        for i in range(num_agents):
            ring_adjacency_matrix[i, (i + 1) % num_agents] = 1
            ring_adjacency_matrix[(i + 1) % num_agents, i] = 1
        np.fill_diagonal(ring_adjacency_matrix, 0)
        matrix_to_return.append(ring_adjacency_matrix)

        return matrix_to_return

    # initialize variables
    cumulative_hits_over_time = [[] for _ in range(6)]
    agent_hits = [[0] * num_agents for _ in range(6)]
    total_hits = [0] * 6
    link_percentage_list = [0.1, 0.5, 0.9]  # 0.1, 0.3, 0.5, 0.7, 0.9

    omega_matrices = [np.ones((num_agents, num_agents)) for _ in range(5)]
    for omega_matrix in omega_matrices:
        np.fill_diagonal(omega_matrix, 0)

    expansion_factor = expansion_times ** (1 / num_steps)
    changes_per_step = []

    # create agents: 5 groups of dynamic agents and 1 group of static agents
    dynamic_agents = [
        _Agent.create(i, env.get_boundary()) for i in range(num_agents * 5)
    ]
    static_agents = [
        _Agent.create(i + 5 * num_agents, env.get_boundary())
        for i in range(num_agents)
    ]
    all_agents = dynamic_agents + static_agents

    # start simulation
    for step in range(num_steps):
        # expand polygon and move the agents
        env.expand_boundary(expansion_factor)
        for agent in all_agents:
            _Agent.update_boundary(agent, env.get_boundary())
        hits_info = [{} for _ in range(5)]
        for agent in all_agents:
            _Agent.move(agent, dt)

        # five group of dynamic agents
        dynamic_agents_groups = [
            dynamic_agents[slice(i * num_agents, (i + 1) * num_agents)]
            for i in range(5)
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

        # update agents with omega matrix, and calculate change in this step
        change_in_this_step = 0
        temp_matrix_list = create_adjcacency_matrix(
            num_agents, link_percentage_list
        )
        for i, group in enumerate(dynamic_agents_groups):
            change, omega_matrices[i] = update_agents(
                group,
                num_agents,
                omega_matrices[i],
                hits_info[i],
                temp_matrix_list[i],
            )
            change_in_this_step += change
        changes_per_step.append(
            change_in_this_step / len(dynamic_agents_groups)
        )

    # plot the convergence graph with change per step
    save_path = (
        save_path_dict["simulation"] + "convergence" + f"_{num_agents}.png"
    )
    plot_convergence(num_steps, changes_per_step, save_path)
    logging.info(
        f"Convergence plot saved at {save_path_dict['simulation']}convergence_"
        f"{num_agents}.png"
    )

    # save task matrix and check its properties
    task_matrix = env.state_transition_matrix
    assert not np.all(task_matrix == 0)
    for row in task_matrix:
        assert np.sum(row) == 1 or np.sum(row) == 0
    np.save(
        save_path_dict["task_matrix"] + str(num_agents) + ".npy", task_matrix
    )
    logging.info(
        f"Task matrix saved at {save_path_dict['task_matrix']}{num_agents}.npy"
    )

    # return cumulative hits over time and max hits
    max_hits = [max(hits) for hits in agent_hits]
    return (
        *cumulative_hits_over_time,
        *max_hits,
    )
