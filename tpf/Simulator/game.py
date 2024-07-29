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
    len_agents: int,
    omega_matrix: np.ndarray,
    hits_info: List[dict],
) -> float:
    change_in_this_step, omega_matrix = Agent.update_omega_matrix(omega_matrix, hits_info)
    for agent in agents:
        Opinion.FJ_update_parameters_adapt(
            agent, len_agents, omega_matrix, agents
        )
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
    cumulative_hits_over_time = [[] for _ in range(6)]
    agent_hits = [[0] * num_agents for _ in range(6)]
    total_hits = [0] * 6

    omega_matrix = np.ones((num_agents, num_agents))
    np.fill_diagonal(omega_matrix, 0)

    dynamic_agents = [
        Agent.create(i, env.get_boundary()) for i in range(num_agents * 5)
    ]
    static_agents = [
        Agent.create(i + num_agents, env.get_boundary())
        for i in range(num_agents)
    ]
    all_agents = dynamic_agents + static_agents
    expansion_factor = expansion_times ** (1 / num_steps)
    changes_per_step = []

    for step in range(num_steps):
        env.expand_boundary(expansion_factor)
        for agent in all_agents:
            Agent.update_boundary(agent, env.get_boundary())
        hits_info = [{} for _ in range(5)]
        for agent in all_agents:
            Agent.move(agent, dt)
        
        dynamic_agents_groups = [
            dynamic_agents[i * num_agents: (i + 1) * num_agents]
            for i in range(5)
        ]
        hits = [
            calculate_hits(static_agents, env.get_target_hole())
        ] + [
            calculate_hits(group, env.get_target_hole())
            for group in dynamic_agents_groups
        ]

        for i, hit_group in enumerate(hits):
            for hit in hit_group:
                idx = hit.id - (i * num_agents if i > 0 else num_agents)
                agent_hits[i][idx] += 1
                if i > 0:
                    hits_info[i - 1][dynamic_agents_groups[i - 1][idx].id] = hit
            total_hits[i] += len(hit_group)
            cumulative_hits_over_time[i].append(total_hits[i])

        old_position = Point(env.hole_x, env.hole_y)
        new_position = env.move_hole(dt)
        env.update_state_transition_matrix(
            old_position.x, old_position.y, new_position.x, new_position.y
        )
        change_in_this_step = update_agents(
            dynamic_agents, num_agents, omega_matrix, hits_info
        )[0]
        changes_per_step.append(change_in_this_step)

    plt.plot(range(num_steps), changes_per_step)
    plt.xlabel("Step")
    plt.ylabel("Change in this step")
    plt.title("Convergence")
    plt.savefig(save_path["simulation"] + "convergence" + f"_{num_agents}.png")
    plt.close()
    logging.info(
        f"Convergence plot saved at {save_path['simulation']}convergence_"
        f"{num_agents}.png"
    )
    task_matrix = env.state_transition_matrix
    assert not np.all(task_matrix == 0)
    for row in task_matrix:
        assert np.sum(row) == 1 or np.sum(row) == 0
    np.save(save_path["task_matrix"] + str(num_agents) + ".npy", task_matrix)
    logging.info(
        f"Task matrix saved at {save_path['task_matrix']}{num_agents}.npy"
    )
    max_hits = [max(hits) for hits in agent_hits]
    return (
        *cumulative_hits_over_time,
        *max_hits,
    )