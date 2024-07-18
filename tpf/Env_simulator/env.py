import math
import random

from shapely.geometry import LineString, Point, Polygon


class Env:
    def __init__(self, width, height, radius, velocity):
        self.width = width
        self.height = height
        self.radius = radius
        self.velocity = velocity
        self.polygon_points = self.generate_convex_polygon(8, width, height)
        self.boundary = Polygon(self.polygon_points)
        self.hole_x, self.hole_y = (
            self.generate_random_position_within_polygon()
        )
        self.ball_speed_x = self.velocity
        self.ball_speed_y = self.velocity

    def generate_convex_polygon(self, num_points, width, height):
        points = [
            (random.randint(0, width), random.randint(0, height))
            for _ in range(num_points)
        ]
        centroid = (
            sum([p[0] for p in points]) / num_points,
            sum([p[1] for p in points]) / num_points,
        )
        points.sort(
            key=lambda p: math.atan2(p[1] - centroid[1], p[0] - centroid[0])
        )
        return points

    def is_point_inside_polygon(self, x, y):
        point = Point(x, y)
        return self.boundary.contains(point)

    def generate_random_position_within_polygon(self):
        min_x, min_y, max_x, max_y = self.boundary.bounds
        while True:
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)
            if self.is_point_inside_polygon(x, y):
                return x, y

    def move_hole(self, dt):
        self.hole_x += self.ball_speed_x * dt
        self.hole_y += self.ball_speed_y * dt

        for i in range(len(self.polygon_points)):
            p1 = self.polygon_points[i]
            p2 = self.polygon_points[(i + 1) % len(self.polygon_points)]
            edge = LineString([p1, p2])
            ball_point = Point(self.hole_x, self.hole_y)

            if edge.distance(ball_point) <= self.radius:
                edge_vector = (p2[0] - p1[0], p2[1] - p1[1])
                edge_length = math.hypot(edge_vector[0], edge_vector[1])
                normal_vector = (
                    -edge_vector[1] / edge_length,
                    edge_vector[0] / edge_length,
                )

                velocity_vector = (self.ball_speed_x, self.ball_speed_y)
                dot_product = (
                    velocity_vector[0] * normal_vector[0]
                    + velocity_vector[1] * normal_vector[1]
                )
                self.ball_speed_x -= 2 * dot_product * normal_vector[0]
                self.ball_speed_y -= 2 * dot_product * normal_vector[1]

                self.hole_x += self.ball_speed_x * dt
                self.hole_y += self.ball_speed_y * dt

                break

    def get_boundary(self):
        return self.boundary

    def get_target_hole(self):
        return Point(self.hole_x, self.hole_y).buffer(self.radius)
