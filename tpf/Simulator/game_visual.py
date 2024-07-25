import logging

import imageio
import networkx as nx

import numpy as np
import pygame
from Agent_simulator.agent import (
    Agent,
)
from Agent_simulator.update_strategy import Para_update_strategies as Opinion
from Env_simulator.env import Env
from Generator.task_top import TaskGraphGenerator as GraphGen
from shapely.geometry import Point
from typing import List
from utils import calculate_hits

logging.basicConfig(level=logging.INFO)


def draw_polygon(screen, boundary, color):
    pygame.draw.polygon(
        screen,
        color,
        [(int(x + 400), int(y + 300)) for x, y in boundary.exterior.coords],
        1,
    )


def draw_hole(screen, env, color):
    pygame.draw.circle(
        screen,
        color,
        (int(env.hole_x + 400), int(env.hole_y + 300)),
        env.radius,
    )


def draw_agents(screen, agents, color):
    for agent in agents:
        pygame.draw.circle(
            screen,
            color,
            (int(agent.position.x + 400), int(agent.position.y + 300)),
            5,
        )


def update_agents(agents: List[Agent], temporary_matrix: np.ndarray, omega_matrix: np.ndarray, hits_info: dict) -> None:
    for agent in agents:
        Opinion.FJ_update_parameters_adapt(agent, temporary_matrix, omega_matrix, agents)
        # Opinion.simple_update_parameters(agent, hits_info)
    Agent.update_omega_matrix(omega_matrix, hits_info, agents)


def run_simulation(width, height, radius, velocity, num_agents, num_steps, dt, save_path):
    env = Env(width, height, radius, velocity)
    cumulative_hits_over_time_normal = []
    cumulative_hits_over_time_special = []
    normal_agent_hits = [0] * num_agents
    special_agent_hits = [0] * num_agents
    total_hits_normal = 0
    total_hits_special = 0

    dynamic_agents = [Agent.create(i, env.get_boundary()) for i in range(num_agents)]
    static_agents = [Agent.create(i + num_agents, env.get_boundary()) for i in range(num_agents)]
    all_agents = dynamic_agents + static_agents

    initial_side_length = 2 * radius
    final_side_length = 4 * radius
    expansion_factor = (final_side_length / initial_side_length) ** (1 / num_steps)

    omega_matrix = np.ones((num_agents, num_agents))
    np.fill_diagonal(omega_matrix, 0)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Needle Throw Simulation")
    clock = pygame.time.Clock()
    FPS = 60

    frames = []

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
        env.move_hole(dt)

        # random temporary_matrix every step to represent the connection between agents
        temporary_matrix = (np.random.rand(len(dynamic_agents), len(dynamic_agents)) < 0.1).astype(int)
        np.fill_diagonal(temporary_matrix, 0)
        update_agents(dynamic_agents, temporary_matrix, omega_matrix, hits_info)

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

    pygame.quit()

    imageio.mimsave(save_path, frames, fps=FPS)

    max_hits_normal = max(normal_agent_hits)
    max_hits_special = max(special_agent_hits)
    return cumulative_hits_over_time_normal, cumulative_hits_over_time_special, max_hits_normal, max_hits_special

