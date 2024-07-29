from typing import Dict, List

import numpy as np
from interface import AgentData
from shapely.geometry import Point


class Para_update_strategies:
    @staticmethod
    # Hegselmann-Krause model
    def HK_update_parameters(
        agent: AgentData, omega_matrix: np.ndarray, agents: list, hit: bool
    ) -> None:
        neighbors = [
            i for i, weight in enumerate(omega_matrix[agent.id]) if weight > 0
        ]
        if neighbors:
            neighbor_info = np.mean(
                [
                    [
                        agents[i].direction,
                        agents[i].speed,
                    ]
                    for i in neighbors
                ],
                axis=0,
            )
            if hit:
                agent.direction = (agent.direction + neighbor_info[0]) / 2
                agent.speed = (agent.speed + neighbor_info[1]) / 2
            else:
                agent.direction = (agent.direction - neighbor_info[0]) / 2
                agent.speed = (agent.speed - neighbor_info[1]) / 2

            max_direction_change = np.pi / 6
            direction_diff = agent.direction - neighbor_info[0]
            if abs(direction_diff) > max_direction_change:
                agent.direction = (
                    neighbor_info[0]
                    + np.sign(direction_diff) * max_direction_change
                )

    @staticmethod
    # common model: change agents' position to the target point
    def simple_update_parameters(
        agent: AgentData, hits_info: Dict[int, Point]
    ) -> None:
        if agent.id in hits_info:
            target_point = hits_info[agent.id]
            direction_to_target = np.arctan2(
                target_point.y - agent.mu.y, target_point.x - agent.mu.x
            )
            distance_to_target = np.hypot(
                target_point.x - agent.mu.x, target_point.y - agent.mu.y
            )
            agent.mu = Point(
                agent.mu.x
                + np.cos(direction_to_target) * distance_to_target * 0.1,
                agent.mu.y
                + np.sin(direction_to_target) * distance_to_target * 0.1,
            )
            agent.theta = max(agent.theta * 0.9, 0.01)  # 逐渐收敛

    @staticmethod
    def FJ_update_parameters(
        agent: AgentData, omega_matrix: np.ndarray, agents: list, hit: bool
    ) -> None:
        neighbors = [
            i for i, weight in enumerate(omega_matrix[agent.id]) if weight > 0
        ]
        if neighbors:
            neighbor_info = np.mean(
                [
                    [
                        agents[i].mu,
                        agents[i].theta,
                    ]
                    for i in neighbors
                ],
                axis=0,
            )
            if hit:
                p = 0.5
                if np.random.rand() < p:
                    agent.mu = neighbor_info[0]
                    agent.theta = neighbor_info[1]

    @staticmethod
    def FJ_update_parameters_adapt(
        agent: AgentData,
        len_dynamic_agents: int,
        omega_matrix: np.ndarray,
        agents: List[AgentData],
    ) -> None:

        update_weight = 0.5
        noise_weight = 0.1
        min_theta = 10
        link_percentage = 0.5

        temporary_matrix = (
            np.random.rand(len_dynamic_agents, len_dynamic_agents)
            < link_percentage
        ).astype(int)
        np.fill_diagonal(temporary_matrix, 0)

        update_matrix = np.multiply(temporary_matrix, omega_matrix)
        neighbors = [
            i for i, weight in enumerate(update_matrix[agent.id]) if weight > 0
        ]

        updated_mu_x = 0
        updated_mu_y = 0
        updated_theta = 0

        if neighbors:
            total_weight = sum(update_matrix[agent.id][i] for i in neighbors)
            if total_weight > 0:
                for i in neighbors:
                    weight = update_matrix[agent.id][i] / total_weight
                    updated_mu_x += weight * agents[i].mu.x
                    updated_mu_y += weight * agents[i].mu.y
                    updated_theta += weight * agents[i].theta

        noise_x = np.random.normal(0, noise_weight)
        noise_y = np.random.normal(0, noise_weight)

        agent.mu = Point(
            update_weight * agent.mu.x
            + (1 - update_weight) * updated_mu_x
            + noise_x,
            update_weight * agent.mu.y
            + (1 - update_weight) * updated_mu_y
            + noise_y,
        )
        agent.theta = max(
            update_weight * agent.theta + (1 - update_weight) * updated_theta,
            min_theta,
        )
        # print(agent.mu, agent.theta)
