# TODO: finish the logic in create a different environment
# like 8 sided polygon or a circle

import logging

import numpy as np
from shapely.affinity import scale
from shapely.geometry import Point, Polygon

logging.basicConfig(level=logging.INFO)


class Env_complex:
    def __init__(
        self,
        width,
        height,
        radius,
        velocity,
        initial_boundary_width,
        expansion_times,
        rdn_seed=None,
    ):
        self.random_state = np.random.RandomState(rdn_seed)
        self.radius = radius
        self.velocity = velocity
        self.width = width
        self.height = height
        self.initial_boundary_width = initial_boundary_width
        self.boundary = self.create_complex_boundary()
        self.hole_x, self.hole_y = (
            self.generate_random_position_within_boundary()
        )
        logging.info(
            f"Generated Target Initial Hole Position:"
            f"({self.hole_x}, {self.hole_y})"
        )
        self.direction = self.random_state.uniform(0, 2 * np.pi)
        self.expansion_times = expansion_times
        self.state_transition_matrix = (
            self.initialize_state_transition_matrix()
        )
        self.time_step = 0

    def create_complex_boundary(self):
        # 生成一个复杂的多边形边界
        points = [
            (
                -self.initial_boundary_width / 2,
                -self.initial_boundary_width / 2,
            ),
            (0, -self.initial_boundary_width / 4),
            (
                self.initial_boundary_width / 2,
                -self.initial_boundary_width / 2,
            ),
            (self.initial_boundary_width / 2, 0),
            (self.initial_boundary_width / 4, self.initial_boundary_width / 2),
            (0, self.initial_boundary_width / 4),
            (
                -self.initial_boundary_width / 4,
                self.initial_boundary_width / 2,
            ),
            (-self.initial_boundary_width / 2, 0),
        ]
        complex_polygon = Polygon(points)
        return complex_polygon

    def generate_random_position_within_boundary(self):
        min_x, min_y, max_x, max_y = self.boundary.bounds
        while True:
            x = self.random_state.uniform(min_x, max_x)
            y = self.random_state.uniform(min_y, max_y)
            point = Point(x, y)
            if self.boundary.contains(point):
                return x, y

    def initialize_state_transition_matrix(self):
        size = int((self.initial_boundary_width * self.expansion_times) ** 2)
        return np.zeros((size, size))

    def get_state_index(self, x, y):
        min_x, min_y, max_x, max_y = self.boundary.bounds
        row = int(
            (y - min_y)
            / (max_y - min_y)
            * (self.initial_boundary_width * self.expansion_times)
        )
        col = int(
            (x - min_x)
            / (max_x - min_x)
            * (self.initial_boundary_width * self.expansion_times)
        )
        return row * self.initial_boundary_width * self.expansion_times + col

    def update_state_transition_matrix(self, prev_x, prev_y, new_x, new_y):
        prev_state = self.get_state_index(prev_x, prev_y)
        new_state = self.get_state_index(new_x, new_y)
        if (
            prev_state >= self.state_transition_matrix.shape[0]
            or new_state >= self.state_transition_matrix.shape[0]
        ):
            return
        self.state_transition_matrix[prev_state, new_state] += 1
        self.state_transition_matrix[
            prev_state
        ] /= self.state_transition_matrix[prev_state].sum()

    def update_velocity(self):
        self.velocity = 1 + np.sin(self.time_step * 0.1)

    def move_hole(self, dt):
        self.update_velocity()
        self.time_step += 1
        new_x = self.hole_x + self.velocity * np.cos(self.direction) * dt
        new_y = self.hole_y + self.velocity * np.sin(self.direction) * dt
        new_position = Point(new_x, new_y)

        if not self.boundary.contains(new_position):
            normal_vector = self.calculate_normal_vector(new_position)
            self.direction = self.reflect_direction(
                self.direction, normal_vector
            )
            new_x = self.hole_x + self.velocity * np.cos(self.direction) * dt
            new_y = self.hole_y + self.velocity * np.sin(self.direction) * dt
            new_position = Point(new_x, new_y)

        self.hole_x, self.hole_y = new_x, new_y
        return new_position

    def calculate_normal_vector(self, point):
        min_x, min_y, max_x, max_y = self.boundary.bounds
        if point.x <= min_x or point.x >= max_x:
            return np.array([1, 0])  # Horizontal wall
        if point.y <= min_y or point.y >= max_y:
            return np.array([0, 1])  # Vertical wall
        return np.array(
            [0, 0]
        )  # Should not reach here if correctly calculated

    def reflect_direction(self, direction, normal_vector):
        direction_vector = np.array([np.cos(direction), np.sin(direction)])
        reflection_vector = (
            direction_vector
            - 2 * np.dot(direction_vector, normal_vector) * normal_vector
        )
        return np.arctan2(reflection_vector[1], reflection_vector[0])

    def expand_boundary(self, factor):
        self.boundary = scale(
            self.boundary, xfact=factor, yfact=factor, origin=(0, 0)
        )

    def get_boundary(self):
        return self.boundary

    def get_target_hole(self):
        return Point(self.hole_x, self.hole_y).buffer(self.radius)
