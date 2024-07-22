from Agent_simulator.agent import (
    Agent,
    Agent_with_initial_direction,
    Agent_with_initial_position,
    Agent_with_initial_speed,
)
from Env_simulator.env import Env
from shapely.geometry import Point


def calculate_hits(needles, target_hole):
    return [needle for needle in needles if target_hole.contains(needle)]


def run_simulation(width, height, radius, velocity, num_agents, num_steps, dt):
    env = Env(width, height, radius, velocity)
    cumulative_hits_over_time_normal = []
    cumulative_hits_over_time_special = []

    normal_agent_hits = [0] * num_agents
    special_agent_hits = [0] * (num_agents // 3 * 3)
    total_hits_normal = 0
    total_hits_special = 0

    initial_position = Point(env.hole_x, env.hole_y)
    initial_speed = velocity
    initial_direction = env.direction

    normal_agents = [Agent(env.get_boundary()) for _ in range(num_agents)]
    agents_type1 = [
        Agent_with_initial_position(env.get_boundary(), initial_position)
        for _ in range(num_agents // 3)
    ]
    agents_type2 = [
        Agent_with_initial_speed(env.get_boundary(), initial_speed)
        for _ in range(num_agents // 3)
    ]
    agents_type3 = [
        Agent_with_initial_direction(env.get_boundary(), initial_direction)
        for _ in range(num_agents // 3)
    ]

    all_agents = normal_agents + agents_type1 + agents_type2 + agents_type3

    initial_side_length = 2 * radius
    final_side_length = 4 * radius
    expansion_factor = (final_side_length / initial_side_length) ** (
        1 / num_steps
    )

    for step in range(num_steps):
        env.expand_boundary(expansion_factor)

        # 更新所有Agent的边界
        for agent in all_agents:
            agent.update_boundary(env.get_boundary())

        for agent in all_agents:
            agent.move(dt)

        needles_normal = [agent.position for agent in normal_agents]
        needles_special = [
            agent.position
            for agent in agents_type1 + agents_type2 + agents_type3
        ]
        hits_normal = calculate_hits(needles_normal, env.get_target_hole())
        hits_special = calculate_hits(needles_special, env.get_target_hole())

        for hit in hits_normal:
            idx = needles_normal.index(hit)
            normal_agent_hits[idx] += 1
        for hit in hits_special:
            idx = needles_special.index(hit)
            special_agent_hits[idx] += 1

        total_hits_normal += len(hits_normal)
        total_hits_special += len(hits_special)

        cumulative_hits_over_time_normal.append(total_hits_normal)
        cumulative_hits_over_time_special.append(total_hits_special)
        env.move_hole(dt)

    max_hits_normal = max(normal_agent_hits)
    max_hits_special = max(special_agent_hits)
    return (
        cumulative_hits_over_time_normal,
        cumulative_hits_over_time_special,
        max_hits_normal,
        max_hits_special,
    )
