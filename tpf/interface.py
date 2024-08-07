from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import UUID

import networkx as nx
from shapely.geometry import Point, Polygon


@dataclass
class GraphData:
    graph: nx.DiGraph
    id: UUID
    type: str  # whether it is a mas graph or a task graph
    name: str


@dataclass
class GraphFeatures:
    id: UUID
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


@dataclass
class TaskGraphFeatures:
    id: UUID
    subtask_dependency_index: float = 0
    node_degree_entropy: float = 0
    path_length_entropy: float = 0
    mutual_information: float = 0


@dataclass
class GraphEval:
    id: UUID
    diameter: int = 0
    dependency: float = 0
    uncertainty: float = 0


@dataclass
class MasEval:
    task_graph: GraphData
    mas_graph: GraphData
    mas_feature: Optional[GraphFeatures] = None
    task_feature: Optional[TaskGraphFeatures] = None
    task_eval: Optional[GraphEval] = None
    mas_eval: Optional[GraphEval] = None
    TCT: float = 0
    TWT: float = 0


@dataclass
class ContiAgent:
    id: int
    position: Point
    direction: float
    speed: float
    # acceleration: float
    boundary: Polygon


@dataclass
class AgentData:
    id: int
    position: Point
    mu: Point
    theta: float
    boundary: Polygon
