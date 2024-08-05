from typing import List

import numpy as np
from interface import AgentData, ContiAgent
from shapely.geometry import Point


class Para_update_strategies:
    @staticmethod
    def simple_update_parameters(
        agent: ContiAgent,
        len_dynamic_agents: int,
        omega_matrix: np.ndarray,
        agents: List[ContiAgent],
        temporary_matrix: np.ndarray,
    ) -> None:
        """
        param agent: agent to update
        param len_dynamic_agents: total number of agents
        param omega_matrix: matrix of weights
        param agents: list of agents
        param temporary_matrix: temporary matrix

        This function is used to update the Continuous movement of agents
        """

        update_weight = 0.9
        beta = 0.9

        update_matrix = np.multiply(temporary_matrix, omega_matrix)

        # 获取所有活跃代理的索引
        active_agents = [
            i
            for i, weight in enumerate(
                update_matrix[agent.id % len_dynamic_agents]
            )
            if weight > 0
        ]

        if len(active_agents) >= 2:
            # 随机选择一个邻居
            neighbors = [i for i in active_agents if i != agent.id]
            Ji = np.random.choice(neighbors)

            # 以概率 β 更新代理的状态
            if np.random.rand() < beta:
                updated_position_x = (
                    update_weight * agents[Ji].position.x
                    + (1 - update_weight) * agent.position.x
                )
                updated_position_y = (
                    update_weight * agents[Ji].position.y
                    + (1 - update_weight) * agent.position.y
                )
                updated_position = Point(
                    updated_position_x, updated_position_y
                )
                updated_speed = (
                    update_weight * agents[Ji].speed
                    + (1 - update_weight) * agent.speed
                )

                if agent.boundary.contains(
                    updated_position
                ) or agent.boundary.touches(updated_position):
                    agent.position = updated_position
                else:
                    print("Agent is out of boundary")
                    agent.position = agent.position

                agent.speed = updated_speed
            else:
                pass
        else:
            pass

    @staticmethod
    def FJ_update_parameters(
        agent: ContiAgent,
        len_dynamic_agents: int,
        omega_matrix: np.ndarray,
        agents: List[ContiAgent],
        temporary_matrix: np.ndarray,
    ) -> None:
        """
        param agent: agent to update
        param len_dynamic_agents: total number of agents
        param omega_matrix: matrix of weights
        param agents: list of agents
        param temporary_matrix: temporary matrix

        This function is used to update the Continuous movement of agents
        """

        update_weight = 0.5
        beta = 0.5

        update_matrix = np.multiply(temporary_matrix, omega_matrix)

        # 获取所有活跃代理的索引
        active_agents = [
            i
            for i, weight in enumerate(
                update_matrix[agent.id % len_dynamic_agents]
            )
            if weight > 0
        ]

        update_position_x = 0
        update_position_y = 0
        update_speed = 0

        if active_agents:
            total_weight = sum(
                update_matrix[agent.id % len_dynamic_agents][i]
                for i in active_agents
            )
            if total_weight > 0:
                for i in active_agents:
                    weight = (
                        update_matrix[agent.id % len_dynamic_agents][i]
                        / total_weight
                    )
                    update_position_x += weight * agents[i].position.x
                    update_position_y += weight * agents[i].position.y
                    update_speed += weight * agents[i].speed

        if np.random.rand() < beta:
            updated_position = Point(
                update_weight * update_position_x
                + (1 - update_weight) * agent.position.x,
                update_weight * update_position_y
                + (1 - update_weight) * agent.position.y,
            )
            updated_speed = (
                update_weight * update_speed
                + (1 - update_weight) * agent.speed
            )

            if agent.boundary.contains(
                updated_position
            ) or agent.boundary.touches(updated_position):
                agent.position = updated_position
                agent.speed = updated_speed
            else:
                # print("Agent is out of boundary")
                agent.position = agent.position

    @staticmethod
    def FJ_update_parameters_adapt(
        agent: AgentData,
        len_dynamic_agents: int,
        omega_matrix: np.ndarray,
        agents: List[AgentData],
        temporary_matrix: np.ndarray,
    ) -> None:

        update_weight = 0.1
        noise_weight = 0.1
        min_theta = 10

        update_matrix = np.multiply(
            temporary_matrix, omega_matrix
        )  # temporary_matrix

        neighbors = [
            i
            for i, weight in enumerate(
                update_matrix[agent.id % len_dynamic_agents]
            )
            if weight > 0
        ]

        updated_mu_x = 0
        updated_mu_y = 0
        updated_theta = 0

        if neighbors:
            total_weight = sum(
                update_matrix[agent.id % len_dynamic_agents][i]
                for i in neighbors
            )
            if total_weight > 0:
                for i in neighbors:
                    weight = (
                        update_matrix[agent.id % len_dynamic_agents][i]
                        / total_weight
                    )
                    updated_mu_x += weight * agents[i].mu.x
                    updated_mu_y += weight * agents[i].mu.y
                    updated_theta += weight * agents[i].theta

        noise_x = np.random.normal(0, noise_weight)
        noise_y = np.random.normal(0, noise_weight)

        agent.mu = Point(
            update_weight * updated_mu_x
            + (1 - update_weight) * agent.mu.x
            + noise_x,
            update_weight * updated_mu_y
            + (1 - update_weight) * agent.mu.y
            + noise_y,
        )
        agent.theta = max(
            update_weight * updated_theta + (1 - update_weight) * agent.theta,
            min_theta,
        )
        # print(agent.mu, agent.theta)
