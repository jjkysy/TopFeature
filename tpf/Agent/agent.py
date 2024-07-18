import numpy as np
from shapely.geometry import Point


class Agent:
    def __init__(self, boundary):
        self.boundary = boundary

    def throw_needle(self):
        return Point(
            np.random.uniform(
                self.boundary.bounds[0], self.boundary.bounds[2]
            ),
            np.random.uniform(
                self.boundary.bounds[1], self.boundary.bounds[3]
            ),
        )
