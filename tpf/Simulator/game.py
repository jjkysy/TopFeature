import logging
from typing import List

import numpy as np
from Agent_simulator.agent import Agent
from Agent_simulator.update_strategy import Para_update_strategies as Opinion
from Env_simulator.env import Env
from matplotlib import pyplot as plt
from shapely.geometry import Point
from utils import calculate_hits

logging.basicConfig(level=logging.INFO)

save_path = {
    "simulation": "plots/simulation_plots/",
    "task_matrix": "plots/task_matrix/",
}


def update_agents(
    agents: List[Agent],
    temporary_matrix: np.ndarray,
    omega_matrix: np.ndarray,
    hits_info: dict,
) -> float:
    for agent in agents:
        Opinion.FJ_update_parameters_adapt(
            agent, temporary_matrix, omega_matrix, agents
        )
        # Opinion.simple_update_parameters(agent, hits_info)
    change_in_this_step = Agent.update_omega_matrix(omega_matrix, hits_info)
    return change_in_this_step


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
    env = Env(
        width,
        height,
        radius,
        velocity,
        initial_boundary_width,
        expansion_times,
    )
    cumulative_hits_over_time_normal = []
    cumulative_hits_over_time_special = []
    normal_agent_hits = [0] * num_agents
    special_agent_hits = [0] * num_agents
    total_hits_normal = 0
    total_hits_special = 0

    dynamic_agents = [
        Agent.create(i, env.get_boundary()) for i in range(num_agents)
    ]
    static_agents = [
        Agent.create(i + num_agents, env.get_boundary())
        for i in range(num_agents)
    ]
    all_agents = dynamic_agents + static_agents

    expansion_factor = expansion_times ** (1 / num_steps)

    omega_matrix = np.ones((num_agents, num_agents))
    np.fill_diagonal(omega_matrix, 0)

    changes_per_step = []

    for step in range(num_steps):
        env.expand_boundary(expansion_factor)

        for agent in all_agents:
            Agent.update_boundary(agent, env.get_boundary())

        hits_info = {}

        for agent in all_agents:
            Agent.move(agent, dt)

        hits_normal = calculate_hits(static_agents, env.get_target_hole())
        hits_special = calculate_hits(dynamic_agents, env.get_target_hole())

        for hit in hits_normal:
            idx = hit.id - num_agents
            normal_agent_hits[idx] += 1
        for hit in hits_special:
            idx = hit.id
            special_agent_hits[idx] += 1
            hits_info[dynamic_agents[idx].id] = hit

        total_hits_normal += len(hits_normal)
        total_hits_special += len(hits_special)

        cumulative_hits_over_time_normal.append(total_hits_normal)
        cumulative_hits_over_time_special.append(total_hits_special)
        old_position = Point(env.hole_x, env.hole_y)
        new_position = env.move_hole(dt)
        env.update_state_transition_matrix(
            old_position.x, old_position.y, new_position.x, new_position.y
        )

        temporary_matrix = (
            np.random.rand(len(dynamic_agents), len(dynamic_agents)) < 0.1
        ).astype(int)
        np.fill_diagonal(temporary_matrix, 0)
        change_in_this_step = update_agents(
            dynamic_agents, temporary_matrix, omega_matrix, hits_info
        )
        changes_per_step.append(change_in_this_step)

    # plot the step and change in this step, to show the convergence
    plt.plot(range(num_steps), changes_per_step)
    plt.xlabel("Step")
    plt.ylabel("Change in this step")
    plt.title("Convergence")
    plt.savefig(save_path["simulation"] + "convergence" + f"_{num_agents}.png")
    plt.close()
    logging.info(
        f"Convergence plot saved at\
            {save_path}simulation/convergence_{num_agents}.png"
    )

    task_matrix = env.state_transition_matrix
    assert not np.all(task_matrix == 0)
    for row in task_matrix:
        assert np.sum(row) == 1 or np.sum(row) == 0
    np.save(save_path["task_matrix"] + str(num_agents) + ".npy", task_matrix)
    logging.info(
        f"Task matrix saved at {save_path}task_matrix/{num_agents}.npy"
    )

    max_hits_normal = max(normal_agent_hits)
    max_hits_special = max(special_agent_hits)
    return (
        cumulative_hits_over_time_normal,
        cumulative_hits_over_time_special,
        max_hits_normal,
        max_hits_special,
    )
