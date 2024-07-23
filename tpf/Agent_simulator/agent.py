import numpy as np
from interface import AgentData
from shapely.geometry import Point, Polygon


class Agent:
    @classmethod
    def _create(cls, agent_id: int, boundary: Polygon) -> AgentData:
        position = cls._generate_random_position_within_polygon(boundary)
        direction = np.random.uniform(0, 2 * np.pi)
        speed = np.random.uniform(1, 5)
        return AgentData(agent_id, position, direction, speed, boundary)

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
        new_x = agent.position.x + agent.speed * np.cos(agent.direction) * dt
        new_y = agent.position.y + agent.speed * np.sin(agent.direction) * dt
        new_position = Point(new_x, new_y)

        if not agent.boundary.contains(new_position):
            normal_vector = Agent.calculate_normal_vector(
                new_position, agent.boundary
            )
            agent.direction = Agent.reflect_direction(
                agent.direction, normal_vector
            )

            new_x = (
                agent.position.x + agent.speed * np.cos(agent.direction) * dt
            )
            new_y = (
                agent.position.y + agent.speed * np.sin(agent.direction) * dt
            )
            new_position = Point(new_x, new_y)

        agent.position = new_position

    @staticmethod
    def calculate_normal_vector(point: Point, boundary: Polygon) -> np.ndarray:
        min_x, min_y, max_x, max_y = boundary.bounds
        if point.x <= min_x or point.x >= max_x:
            return np.array([1, 0])  # Horizontal wall
        if point.y <= min_y or point.y >= max_y:
            return np.array([0, 1])  # Vertical wall
        return np.array(
            [0, 0]
        )  # Should not reach here if correctly calculated

    @staticmethod
    def reflect_direction(
        direction: float, normal_vector: np.ndarray
    ) -> float:
        direction_vector = np.array([np.cos(direction), np.sin(direction)])
        reflection_vector = (
            direction_vector
            - 2 * np.dot(direction_vector, normal_vector) * normal_vector
        )
        return np.arctan2(reflection_vector[1], reflection_vector[0])

    @staticmethod
    def update_boundary(agent: AgentData, new_boundary: Polygon) -> None:
        agent.boundary = new_boundary
        if not new_boundary.contains(agent.position):
            agent.position = Agent._generate_random_position_within_polygon(
                new_boundary
            )


class Agent_with_initial_position(Agent):
    @classmethod
    def create(
        cls, agent_id: int, boundary: Polygon, initial_position: Point
    ) -> "AgentData":
        agent_data = super()._create(agent_id, boundary)
        return AgentData(
            agent_id,
            initial_position,
            agent_data.direction,
            agent_data.speed,
            boundary,
        )


class Agent_with_initial_speed(Agent):
    @classmethod
    def create(
        cls, agent_id: int, boundary: Polygon, initial_speed: float
    ) -> "AgentData":
        agent_data = super()._create(agent_id, boundary)
        return AgentData(
            agent_id,
            agent_data.position,
            agent_data.direction,
            initial_speed,
            boundary,
        )


class Agent_with_initial_direction(Agent):
    @classmethod
    def create(
        cls, agent_id: int, boundary: Polygon, initial_direction: float
    ) -> "AgentData":
        agent_data = super()._create(agent_id, boundary)
        return AgentData(
            agent_id,
            agent_data.position,
            initial_direction,
            agent_data.speed,
            boundary,
        )
