import logging

import imageio
import networkx as nx
import pygame
import numpy as np
from Agent_simulator.agent import (
    Agent,
    Agent_with_initial_direction,
    Agent_with_initial_position,
    Agent_with_initial_speed,
)
from Agent_simulator.update_strategy import Para_update_strategies
from Env_simulator.env import Env
from Generator.task_top import TaskGraphGenerator as GraphGen
from shapely.geometry import Point
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


def update_agents_paths(special_agents, omega_matrix, hits_info):
    for agent in special_agents:
        # hit = agent.id in hits_info
        # Para_update_strategies.HK_update_parameters(
        #     agent, omega_matrix, special_agents, hit
        # )
        Para_update_strategies.simple_update_parameters(agent, hits_info)


def run_simulation(
    width, height, radius, velocity, num_agents, num_steps, dt, save_path
):
    env = Env(width, height, radius, velocity)
    cumulative_hits_over_time_normal = []
    cumulative_hits_over_time_special = []

    normal_agent_hits = [0] * num_agents
    special_agent_hits = [0] * (num_agents // 3 * 3)
    total_hits_normal = 0
    total_hits_special = 0

    initial_position = Point(env.hole_x, env.hole_y)
    initial_speed = velocity
    initial_direction = env.direction

    agents_type1 = [
        Agent_with_initial_position.create(
            i, env.get_boundary(), initial_position
        )
        for i in range(num_agents // 3)
    ]
    agents_type2 = [
        Agent_with_initial_speed.create(
            num_agents // 3 + i, env.get_boundary(), initial_speed
        )
        for i in range(num_agents // 3)
    ]
    agents_type3 = [
        Agent_with_initial_direction.create(
            2 * num_agents // 3 + i, env.get_boundary(), initial_direction
        )
        for i in range(num_agents // 3)
    ]
    normal_agents = [
        Agent._create(num_agents + i, env.get_boundary())
        for i in range(num_agents)
    ]

    special_agents = agents_type1 + agents_type2 + agents_type3
    all_agents = normal_agents + special_agents

    initial_side_length = 2 * radius
    final_side_length = 4 * radius
    expansion_factor = (final_side_length / initial_side_length) ** (
        1 / num_steps
    )

    # G = GraphGen.generate_layer_hybrid_tasks(num_agents, 1)[0].graph
    # omega_matrix = nx.to_numpy_array(G)

    G = nx.complete_graph(num_agents)
    for i in range(num_agents):
        weights = np.random.rand(num_agents)
        weights /= np.sum(weights)
        nx.set_node_attributes(G, {i: {"weights": weights}})
    omega_matrix = nx.to_numpy_array(G)

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

        needles_normal = [agent.position for agent in normal_agents]
        needles_special = [agent.position for agent in special_agents]
        hits_normal = calculate_hits(needles_normal, env.get_target_hole())
        hits_special = calculate_hits(needles_special, env.get_target_hole())

        for hit in hits_normal:
            idx = needles_normal.index(hit)
            normal_agent_hits[idx] += 1
        for hit in hits_special:
            idx = needles_special.index(hit)
            special_agent_hits[idx] += 1
            hits_info[special_agents[idx].id] = env.get_target_hole().centroid

        total_hits_normal += len(hits_normal)
        total_hits_special += len(hits_special)

        cumulative_hits_over_time_normal.append(total_hits_normal)
        cumulative_hits_over_time_special.append(total_hits_special)
        env.move_hole(dt)
        print(hits_info)
        update_agents_paths(special_agents, omega_matrix, hits_info)
        # update_agents_paths(special_agents, hits_info)

        screen.fill((255, 255, 255))
        draw_polygon(screen, env.get_boundary(), (0, 0, 0))
        draw_hole(screen, env, (255, 0, 0))
        draw_agents(screen, normal_agents, (0, 0, 255))
        draw_agents(screen, special_agents, (0, 255, 0))
        pygame.display.flip()
        clock.tick(FPS)

        frame = pygame.surfarray.array3d(screen)
        frame = frame.transpose([1, 0, 2])
        frames.append(frame)

    pygame.quit()

    imageio.mimsave(save_path, frames, fps=FPS)

    max_hits_normal = max(normal_agent_hits)
    max_hits_special = max(special_agent_hits)
    return (
        cumulative_hits_over_time_normal,
        cumulative_hits_over_time_special,
        max_hits_normal,
        max_hits_special,
    )
