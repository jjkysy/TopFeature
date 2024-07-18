import pygame
from Agent.agent import Agent
from Env_simulator.env import Env
from shapely.geometry import Point


def calculate_hits(needles, target_hole):
    return sum(1 for needle in needles if target_hole.contains(needle))


def draw_polygon(screen, env, color):
    pygame.draw.polygon(screen, color, env.polygon_points, 1)


def draw_hole(screen, env, color):
    pygame.draw.circle(
        screen, color, (int(env.hole_x), int(env.hole_y)), env.radius
    )


def draw_agents(screen, needles, special_needle, color_normal, color_special):
    for needle in needles:
        pygame.draw.circle(
            screen, color_normal, (int(needle.x), int(needle.y)), 5
        )
    pygame.draw.circle(
        screen,
        color_special,
        (int(special_needle.x), int(special_needle.y)),
        5,
    )


def visualize(env, needles, special_needle, screen):
    screen.fill((255, 255, 255))
    draw_polygon(screen, env, (0, 0, 0))
    draw_hole(screen, env, (255, 0, 0))
    draw_agents(screen, needles, special_needle, (0, 255, 0), (255, 255, 0))
    pygame.display.flip()


def run_simulation(width, height, radius, velocity, num_agents, num_steps, dt):
    env = Env(width, height, radius, velocity)
    cumulative_hits_over_time = []
    special_cumulative_hits_over_time = []

    total_hits = 0
    special_total_hits = 0
    running = True
    step = 0

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Needle Throw Simulation")
    clock = pygame.time.Clock()
    FPS = 60

    while running and step < num_steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        needles = [
            Agent(env.get_boundary()).throw_needle() for _ in range(num_agents)
        ]
        special_needle = Point(env.hole_x, env.hole_y)
        hits = calculate_hits(needles, env.get_target_hole())
        total_hits += hits
        special_hits = 1
        special_total_hits += special_hits

        cumulative_hits_over_time.append(total_hits)
        special_cumulative_hits_over_time.append(special_total_hits)
        env.move_hole(dt)

        visualize(env, needles, special_needle, screen)
        pygame.time.delay(100)

        step += 1
        clock.tick(FPS)

    pygame.quit()

    return cumulative_hits_over_time, special_cumulative_hits_over_time
