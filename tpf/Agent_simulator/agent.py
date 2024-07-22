import numpy as np
from shapely.geometry import Point, Polygon


class Agent:
    def __init__(self, boundary: Polygon):
        self.boundary = boundary
        self.position = self._generate_random_position_within_polygon()
        self.direction = np.random.uniform(0, 2 * np.pi)
        self.speed = np.random.uniform(1, 5)

    def _generate_random_position_within_polygon(self):
        min_x, min_y, max_x, max_y = self.boundary.bounds
        while True:
            x = np.random.uniform(min_x, max_x)
            y = np.random.uniform(min_y, max_y)
            point = Point(x, y)
            if self.boundary.contains(point):
                return point

    def move(self, dt):
        new_x = self.position.x + self.speed * np.cos(self.direction) * dt
        new_y = self.position.y + self.speed * np.sin(self.direction) * dt
        new_position = Point(new_x, new_y)

        if not self.boundary.contains(new_position):
            self.direction = (self.direction + np.pi) % (2 * np.pi)
            new_x = self.position.x + self.speed * np.cos(self.direction) * dt
            new_y = self.position.y + self.speed * np.sin(self.direction) * dt
            new_position = Point(new_x, new_y)

            if not self.boundary.contains(new_position):
                self.direction = (self.direction + np.pi) % (2 * np.pi)
                new_x = (
                    self.position.x + self.speed * np.cos(self.direction) * dt
                )
                new_y = (
                    self.position.x + self.speed * np.sin(self.direction) * dt
                )
                new_position = Point(new_x, new_y)

        self.position = new_position

    def update_boundary(self, new_boundary):
        self.boundary = new_boundary
        if not self.boundary.contains(self.position):
            self.position = self._generate_random_position_within_polygon()

    def throw_needle(self):
        return self.position


class Agent_with_initial_position(Agent):
    def __init__(self, boundary: Polygon, initial_position: Point):
        super().__init__(boundary)
        self.position = initial_position

    def move(self, dt):
        super().move(dt)


class Agent_with_initial_speed(Agent):
    def __init__(self, boundary: Polygon, initial_speed: float):
        super().__init__(boundary)
        self.speed = initial_speed

    def move(self, dt):
        super().move(dt)


class Agent_with_initial_direction(Agent):
    def __init__(self, boundary: Polygon, initial_direction: float):
        super().__init__(boundary)
        self.direction = initial_direction

    def move(self, dt):
        super().move(dt)
