import pygame
import random
import math
from shapely.geometry import Point, Polygon, LineString

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Hole properties
HOLE_RADIUS = 20

# Ball properties
BALL_RADIUS = 5
ball_speed_x = 3
ball_speed_y = 3

# Success rate
total_shots = 0
successful_shots = 0

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Through Ball Game")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Generate convex polygon boundary
def generate_convex_polygon(num_points, width, height):
    points = [(random.randint(0, width), random.randint(0, height)) for _ in range(num_points)]
    centroid = (sum([p[0] for p in points]) / num_points, sum([p[1] for p in points]) / num_points)
    points.sort(key=lambda p: math.atan2(p[1] - centroid[1], p[0] - centroid[0]))
    return points

num_points = 8
polygon_points = generate_convex_polygon(num_points, SCREEN_WIDTH, SCREEN_HEIGHT)
polygon = Polygon(polygon_points)

# Function to check if point is inside polygon
def is_point_inside_polygon(x, y, polygon):
    point = Point(x, y)
    return polygon.contains(point)

# Generate initial hole position within the polygon
def generate_random_position_within_polygon(polygon):
    min_x, min_y, max_x, max_y = polygon.bounds
    while True:
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        if is_point_inside_polygon(x, y, polygon):
            return x, y

hole_x, hole_y = generate_random_position_within_polygon(polygon)

# Agent properties
agent_x, agent_y = generate_random_position_within_polygon(polygon)

def move_hole():
    global hole_x, hole_y, ball_speed_x, ball_speed_y
    hole_x += ball_speed_x
    hole_y += ball_speed_y

    # Check for collision with polygon edges and reflect velocity vector
    for i in range(len(polygon_points)):
        p1 = polygon_points[i]
        p2 = polygon_points[(i + 1) % len(polygon_points)]
        edge = LineString([p1, p2])
        ball_point = Point(hole_x, hole_y)

        if edge.distance(ball_point) <= HOLE_RADIUS:
            # Calculate normal vector of the edge
            edge_vector = (p2[0] - p1[0], p2[1] - p1[1])
            edge_length = math.hypot(edge_vector[0], edge_vector[1])
            normal_vector = (-edge_vector[1] / edge_length, edge_vector[0] / edge_length)

            # Reflect the ball's velocity vector off the edge
            velocity_vector = (ball_speed_x, ball_speed_y)
            dot_product = (velocity_vector[0] * normal_vector[0] + velocity_vector[1] * normal_vector[1])
            ball_speed_x -= 2 * dot_product * normal_vector[0]
            ball_speed_y -= 2 * dot_product * normal_vector[1]

            # Ensure the ball is moved inside the boundary after collision
            hole_x += ball_speed_x
            hole_y += ball_speed_y

            break

def draw_polygon():
    pygame.draw.polygon(screen, BLACK, polygon_points, 1)

def draw_hole():
    pygame.draw.circle(screen, RED, (int(hole_x), int(hole_y)), HOLE_RADIUS)

def draw_agent():
    pygame.draw.circle(screen, GREEN, (int(agent_x), int(agent_y)), BALL_RADIUS)

def check_collision(ball_x, ball_y):
    global successful_shots
    distance = math.hypot(ball_x - hole_x, ball_y - hole_y)
    if distance <= HOLE_RADIUS:
        successful_shots += 1
        return True
    return False

def game_loop():
    global total_shots

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                total_shots += 1
                if check_collision(mouse_x, mouse_y):
                    print("Hit!")
                else:
                    print("Miss!")

        screen.fill(WHITE)
        draw_polygon()
        draw_hole()
        draw_agent()

        move_hole()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
