import numpy as np
from shapely.affinity import scale
from shapely.geometry import Point, Polygon


class Env:
    def __init__(self, width, height, radius, velocity):
        self.radius = radius
        self.velocity = velocity
        self.width = width
        self.height = height
        self.boundary = self.create_square_boundary(radius)
        self.hole_x, self.hole_y = (
            self.generate_random_position_within_boundary()
        )
        self.direction = np.random.uniform(0, 2 * np.pi)

    def create_square_boundary(self, radius):
        side_length = (
            10 * radius
        )  # Initial side length based on the diameter of the hole
        square = Polygon(
            [
                (-side_length / 2, -side_length / 2),
                (side_length / 2, -side_length / 2),
                (side_length / 2, side_length / 2),
                (-side_length / 2, side_length / 2),
            ]
        )
        return square

    def generate_random_position_within_boundary(self):
        min_x, min_y, max_x, max_y = self.boundary.bounds
        while True:
            x = np.random.uniform(min_x, max_x)
            y = np.random.uniform(min_y, max_y)
            point = Point(x, y)
            if self.boundary.contains(point):
                return x, y

    def move_hole(self, dt):
        new_x = self.hole_x + self.velocity * np.cos(self.direction) * dt
        new_y = self.hole_y + self.velocity * np.sin(self.direction) * dt
        new_position = Point(new_x, new_y)

        if not self.boundary.contains(new_position):
            self.direction = np.pi - self.direction
            new_x = self.hole_x + self.velocity * np.cos(self.direction) * dt
            new_y = self.hole_y + self.velocity * np.sin(self.direction) * dt
            new_position = Point(new_x, new_y)
            if not self.boundary.contains(new_position):
                self.direction = -self.direction
                new_x = (
                    self.hole_x + self.velocity * np.cos(self.direction) * dt
                )
                new_y = (
                    self.hole_y + self.velocity * np.sin(self.direction) * dt
                )
                new_position = Point(new_x, new_y)

        self.hole_x, self.hole_y = new_x, new_y

    def expand_boundary(self, factor):
        self.boundary = scale(
            self.boundary, xfact=factor, yfact=factor, origin=(0, 0)
        )

    def get_boundary(self):
        return self.boundary

    def get_target_hole(self):
        return Point(self.hole_x, self.hole_y).buffer(self.radius)
