##############################################################################
# Randomly create task topologies to represent work flow
# For now, we category the task topologies as follows:
# 1. Linear task, 2. Parallel task, 3. Hybrid task
# We want to generate these 3 types of task topologies
# It will form a finite set of task topologies
# Further we calculate their dependencies and so on(if any)
# to be filled @yang
##############################################################################
import random
import uuid
from typing import List

import networkx as nx
import numpy as np
from interface import GraphData


class TaskGraphGenerator:
    @classmethod
    def generate_random_weights(cls, num_weights) -> np.ndarray:
        weights = np.random.dirichlet(np.ones(num_weights), size=1)[0]
        return weights

    @classmethod
    def generate_linear_tasks(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        linear_graph = []
        for i in range(n_graph):
            linear = nx.DiGraph()
            for j in range(n_node - 1):
                # add random weight to the edge
                linear.add_edge(j + 1, j, weight=1)
            linear_graph.append(
                GraphData(
                    graph=linear,
                    name=f"linear_{i}",
                    id=uuid.uuid4(),
                    type="task",
                )
            )
        return linear_graph

    @classmethod
    def generate_parallel_tasks(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        parallel_graph = []
        for i in range(n_graph):
            parallel = nx.DiGraph()
            for j in range(1, n_node):
                parallel.add_edge(j, 0, weight=1 / n_node - 1)
            parallel_graph.append(
                GraphData(
                    graph=parallel,
                    name=f"parallel_{i}",
                    id=uuid.uuid4(),
                    type="task",
                )
            )
        return parallel_graph

    @classmethod
    def generate_hybrid_tasks(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        hybrid_graph = []
        for i in range(n_graph):
            hybrid = nx.DiGraph()
            a = random.choice(range(1, n_node))
            for j in range(a):
                hybrid.add_edge(j + 1, j)
            for j in range(a, n_node):
                hybrid.add_edge(j, 0)
            for node in hybrid.nodes:
                out_edges = list(hybrid.out_edges(node))
                if len(out_edges) > 0:
                    weights = cls.generate_random_weights(len(out_edges))
                    for edge, weight in zip(out_edges, weights):
                        hybrid[edge[0]][edge[1]]["weight"] = weight
            hybrid_graph.append(
                GraphData(
                    graph=hybrid,
                    name=f"hybrid_{i}",
                    id=uuid.uuid4(),
                    type="task",
                )
            )
        return hybrid_graph

    @classmethod
    def generate_layer_hybrid_tasks(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        layer_hybrid_graph = []
        for i in range(n_graph):
            layer_hybrid = nx.DiGraph()
            layer_hybrid.add_edge(1, 0)
            current_node = 0
            for j in range(2, n_node):
                latest_node = j
                choice = random.choice([0, 1])
                if choice == 0:
                    layer_hybrid.add_edge(latest_node, current_node)
                else:
                    current_node += 1
                    layer_hybrid.add_edge(latest_node, current_node)
            for node in layer_hybrid.nodes:
                out_edges = list(layer_hybrid.out_edges(node))
                if len(out_edges) > 0:
                    weights = cls.generate_random_weights(len(out_edges))
                    for edge, weight in zip(out_edges, weights):
                        layer_hybrid[edge[0]][edge[1]]["weight"] = weight
            layer_hybrid_graph.append(
                GraphData(
                    graph=layer_hybrid,
                    name=f"layer_hybrid_{i}",
                    id=uuid.uuid4(),
                    type="task",
                )
            )
        return layer_hybrid_graph
