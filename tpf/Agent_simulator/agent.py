import numpy as np
from interface import AgentData
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
        increase_factor=0.1,
        decay_factor=0.1,
    ) -> float:
        old_omega_matrix = np.copy(omega_matrix)
        for agent_id in range(omega_matrix.shape[0]):
            for neighbor_id in range(omega_matrix.shape[1]):
                if agent_id != neighbor_id:
                    if agent_id in hits_info:
                        omega_matrix[agent_id][neighbor_id] += increase_factor
                    omega_matrix[agent_id][neighbor_id] *= 1 - decay_factor

        # to prove convergence
        total_change = 0
        for i in range(omega_matrix.shape[0]):
            for j in range(omega_matrix.shape[1]):
                total_change += abs(
                    omega_matrix[i][j] - old_omega_matrix[i][j]
                )
        return total_change
