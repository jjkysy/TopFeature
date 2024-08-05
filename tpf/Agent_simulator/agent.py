from typing import Tuple

import numpy as np
from interface import AgentData, ContiAgent
from shapely.geometry import Point, Polygon


class Agent:
    @classmethod
    def create(cls, agent_id: int, boundary: Polygon) -> AgentData:
        position = cls._generate_random_position_within_polygon(boundary)
        mu = position
        # theta is chosen randomly from 10 to 100
        theta = np.random.uniform(10, 100)
        return AgentData(agent_id, position, mu, theta, boundary)

    @staticmethod
    def _generate_random_position_within_polygon(boundary: Polygon) -> Point:
        min_x, min_y, max_x, max_y = boundary.bounds
        while True:
            x = np.random.uniform(min_x, max_x)
            y = np.random.uniform(min_y, max_y)
            point = Point(x, y)
            if boundary.contains(point):
                return point

    @staticmethod
    def move(agent: AgentData, dt: float) -> None:
        agent.theta = max(agent.theta, 0.01)
        new_x = np.random.normal(agent.mu.x, agent.theta)
        new_y = np.random.normal(agent.mu.y, agent.theta)
        new_position = Point(new_x, new_y)

        if agent.boundary.contains(new_position):
            agent.position = new_position

    @staticmethod
    def update_boundary(agent: AgentData, new_boundary: Polygon) -> None:
        agent.boundary = new_boundary
        if not new_boundary.contains(agent.position):
            agent.position = Agent._generate_random_position_within_polygon(
                new_boundary
            )

    @staticmethod
    def update_omega_matrix(
        omega_matrix: np.ndarray,
        hits_info: dict,
        increase_factor=0.01,
        decay_factor=0.01,
    ) -> Tuple[float, np.ndarray]:
        old_omega_matrix = np.copy(omega_matrix)
        total_change = 0

        for agent_id in range(omega_matrix.shape[0]):
            for neighbor_id in range(omega_matrix.shape[1]):
                if agent_id != neighbor_id:
                    if agent_id in hits_info:
                        omega_matrix[agent_id][neighbor_id] += increase_factor
                    else:
                        omega_matrix[agent_id][neighbor_id] *= 1 - decay_factor
                    total_change += abs(
                        omega_matrix[agent_id][neighbor_id]
                        - old_omega_matrix[agent_id][neighbor_id]
                    )

        return total_change, omega_matrix


class _Agent:
    @classmethod
    def create(cls, agent_id: int, boundary: Polygon) -> ContiAgent:
        position = cls.generate_random_position_within_polygon(boundary)
        direction = np.random.uniform(0, 2 * np.pi)
        speed = np.random.uniform(1, 2)
        return ContiAgent(agent_id, position, direction, speed, boundary)

    @staticmethod
    def generate_random_position_within_polygon(boundary: Polygon) -> Point:
        min_x, min_y, max_x, max_y = boundary.bounds
        while True:
            x = np.random.uniform(min_x, max_x)
            y = np.random.uniform(min_y, max_y)
            point = Point(x, y)
            if boundary.contains(point):
                return point

    @staticmethod
    def move(agent, dt):
        new_x = agent.position.x + agent.speed * np.cos(agent.direction) * dt
        new_y = agent.position.y + agent.speed * np.sin(agent.direction) * dt
        new_position = Point(new_x, new_y)

        # 检查是否超出边界
        if not agent.boundary.contains(new_position):
            # 反弹逻辑
            if new_position.x < agent.boundary.bounds[0]:
                new_x = agent.boundary.bounds[0]
                agent.direction = np.pi - agent.direction
            elif new_position.x > agent.boundary.bounds[2]:
                new_x = agent.boundary.bounds[2]
                agent.direction = np.pi - agent.direction
            if new_position.y < agent.boundary.bounds[1]:
                new_y = agent.boundary.bounds[1]
                agent.direction = -agent.direction
            elif new_position.y > agent.boundary.bounds[3]:
                new_y = agent.boundary.bounds[3]
                agent.direction = -agent.direction

            # 调整位置回边界内
            new_position = Point(new_x, new_y)

        agent.position = new_position

    @staticmethod
    def update_boundary(agent: ContiAgent, new_boundary: Polygon) -> None:
        agent.boundary = new_boundary
        if not new_boundary.contains(agent.position):
            agent.position = _Agent.generate_random_position_within_polygon(
                new_boundary
            )

    @staticmethod
    def update_omega_matrix(
        omega_matrix: np.ndarray,
        hits_info: dict,
        increase_factor=0.01,
        decay_factor=0.01,
    ) -> Tuple[float, np.ndarray]:
        old_omega_matrix = np.copy(omega_matrix)
        total_change = 0

        for agent_id in range(omega_matrix.shape[0]):
            for neighbor_id in range(omega_matrix.shape[1]):
                if agent_id != neighbor_id:
                    if agent_id in hits_info:
                        omega_matrix[agent_id][neighbor_id] += increase_factor
                    else:
                        omega_matrix[agent_id][neighbor_id] *= 1 - decay_factor
                    total_change += abs(
                        omega_matrix[agent_id][neighbor_id]
                        - old_omega_matrix[agent_id][neighbor_id]
                    )

        return total_change, omega_matrix
