import logging
from typing import List

import imageio
import numpy as np
import pygame
from Agent_simulator.agent import Agent
from Agent_simulator.update_strategy import Para_update_strategies as Opinion
from Env_simulator.env import Env
from matplotlib import pyplot as plt
from shapely.geometry import Point
from utils import calculate_hits

logging.basicConfig(level=logging.INFO)


def update_agents(
    agents: List[Agent],
    len_agents: int,
    omega_matrix: np.ndarray,
    hits_info: dict,
) -> float:
    for agent in agents:
        Opinion.FJ_update_parameters_adapt(
            agent, len_agents, omega_matrix, agents
        )
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
    FPS,
    expansion_times,
    # learning_rate,
    # theta,
    # gamma,
    # epsilon,
    # batch_size,
    # q_network_params,
):

    def draw_polygon(screen, boundary, color):
        pygame.draw.polygon(
            screen,
            color,
            [
                (int(x + width / 2), int(y + height / 2))
                for x, y in boundary.exterior.coords
            ],
            1,
        )

    def draw_hole(screen, env, color):
        pygame.draw.circle(
            screen,
            color,
            (int(env.hole_x + width / 2), int(env.hole_y + height / 2)),
            env.radius,
        )

    def draw_agents(screen, agents, color):
        for agent in agents:
            pygame.draw.circle(
                screen,
                color,
                (
                    int(agent.position.x + width / 2),
                    int(agent.position.y + height / 2),
                ),
                1,
            )

    save_path = "plots/animation/" + f"simulation_{num_agents}.gif"
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

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Needle Throw Simulation")
    clock = pygame.time.Clock()
    FPS = 60

    frames = []
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
        # print("Now the speed is: ", env.velocity)

        change_in_this_step = update_agents(
            dynamic_agents, num_agents, omega_matrix, hits_info
        )
        changes_per_step.append(change_in_this_step)

        screen.fill((255, 255, 255))
        draw_polygon(screen, env.get_boundary(), (0, 0, 0))
        draw_hole(screen, env, (255, 0, 0))
        draw_agents(screen, static_agents, (0, 0, 255))
        draw_agents(screen, dynamic_agents, (0, 255, 0))
        pygame.display.flip()
        clock.tick(FPS)

        frame = pygame.surfarray.array3d(screen)
        frame = frame.transpose([1, 0, 2])
        frames.append(frame)

    # plot the step and change in this step, to show the convergence
    plt.plot(range(num_steps), changes_per_step)
    plt.xlabel("Step")
    plt.ylabel("Change in this step")
    plt.title("Convergence")
    plt.savefig("plots/simulation_plots/convergence" + f"_{num_agents}.png")
    plt.close()

    pygame.quit()

    imageio.mimsave(save_path, frames, fps=FPS)

    task_matrix = env.state_transition_matrix
    # print(task_matrix)
    # assert not all zero
    assert not np.all(task_matrix == 0)
    # assert sum of each row is 1 or 0
    for row in task_matrix:
        assert np.sum(row) == 1 or np.sum(row) == 0

    max_hits_normal = max(normal_agent_hits)
    max_hits_special = max(special_agent_hits)
    return (
        cumulative_hits_over_time_normal,
        cumulative_hits_over_time_special,
        max_hits_normal,
        max_hits_special,
    )
