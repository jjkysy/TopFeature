from dataclasses import dataclass, field
from typing import Any, Dict

import networkx as nx


@dataclass
class GraphData:
    graph: nx.DiGraph
    name: str


@dataclass
class GraphFeatures:
    name: str
    degree_centrality: Dict[Any, float] = field(default_factory=dict)
    betweenness_centrality: Dict[Any, float] = field(default_factory=dict)
    closeness_centrality: Dict[Any, float] = field(default_factory=dict)
    edge_betweenness_centrality: Dict[Any, float] = field(default_factory=dict)
    eccentricity: Dict[Any, int] = field(default_factory=dict)
    diameter: int = 0
    radius: int = 0
    node_independence: Dict[Any, float] = field(default_factory=dict)
    second_order_centrality: Dict[Any, float] = field(default_factory=dict)
    clustering_coefficient: Dict[Any, float] = field(default_factory=dict)
    average_betweenness_centrality: float = 0
    average_closeness_centrality: float = 0
    average_degree_centrality: float = 0
    average_node_independence: float = 0
    average_second_order_centrality: float = 0
    average_clustering_coefficient: float = 0
    # add more features here (if any)
