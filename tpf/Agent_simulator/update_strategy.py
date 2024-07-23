from typing import Dict

import numpy as np
from interface import AgentData


class Para_update_strategies:
    @staticmethod
    # Hegselmann-Krause model
    def HK_update_parameters(
        agent: AgentData, omega_matrix: np.ndarray, agents: list, hit: bool
    ) -> None:
        neighbors = [
            i for i, weight in enumerate(omega_matrix[agent.id]) if weight > 0
        ]
        if neighbors:
            neighbor_info = np.mean(
                [
                    [
                        agents[i].direction,
                        agents[i].speed,
                    ]
                    for i in neighbors
                ],
                axis=0,
            )
            if hit:
                agent.direction = (agent.direction + neighbor_info[0]) / 2
                agent.speed = (agent.speed + neighbor_info[1]) / 2
            else:
                agent.direction = (agent.direction - neighbor_info[0]) / 2
                agent.speed = (agent.speed - neighbor_info[1]) / 2

            max_direction_change = np.pi / 6
            direction_diff = agent.direction - neighbor_info[0]
            if abs(direction_diff) > max_direction_change:
                agent.direction = (
                    neighbor_info[0]
                    + np.sign(direction_diff) * max_direction_change
                )

    @staticmethod
    # common model: change agents' direction when some agent hits
    def simple_update_parameters(agent: AgentData, hits_info: Dict) -> None:
        if agent.id in hits_info:
            direction_to_target = np.arctan2(
                hits_info[agent.id].y - agent.position.y,
                hits_info[agent.id].x - agent.position.x,
            )
            agent.direction = direction_to_target
