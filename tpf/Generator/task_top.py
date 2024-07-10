##############################################################################
# Randomly create task topologies to represent work flow
# For now, we category the task topologies as follows:
# 1. Linear task, 2. Parallel task, 3. Hybrid task
# We want to generate these 3 types of task topologies
# It will form a finite set of task topologies
# Further we calculate their dependencies and so on(if any)
# to be filled @yang
##############################################################################
import pickle
from typing import List
import random

import networkx as nx
from typing import List, Callable, Dict
import random
from tpf.interface import GraphData
import uuid


class TaskGraphGenerator:
    @classmethod
    def generate_linear_tasks(cls, n_node: int, n_graph: int) -> List[GraphData]:
        linear_graph = []
        linear = nx.DiGraph()
        for i in range(n_graph):
            for j in range(n_node-1):
                # add random weight to the edge
                linear.add_edge(j, j+1, weight=random.random())
            linear_graph.append(
                GraphData(graph=linear, name=f"linear_{i}", id=uuid.uuid4(), type='task')
            )
        return linear_graph

    @classmethod
    def generate_parallel_tasks(cls, n_node: int, n_graph: int) -> List[GraphData]:
        parallel_graph = []
        parallel = nx.DiGraph()
        for i in range(n_graph):
            for j in range(1, n_node):
                parallel.add_edge(0, j, weight=random.random())
            parallel_graph.append(
                GraphData(graph=parallel, name=f"parallel_{i}", id=uuid.uuid4(), type='task')
            )
        return parallel_graph

    @classmethod
    def generate_hybrid_tasks(cls, n_node: int, n_graph: int) -> List[GraphData]:
        hybrid_graph = []
        for i in range(n_graph):
            hybrid = nx.DiGraph()
            a = random.choice(range(1, n_node))
            for j in range(a):
                hybrid.add_edge(j, j+1, weight=random.random())
            for j in range(a, n_node):
                hybrid.add_edge(0, j, weight=random.random())
            hybrid_graph.append(
                GraphData(graph=hybrid, name=f"hybrid_{i}", id=uuid.uuid4(), type='task')
            )
        return hybrid_graph

    # TODO: improve the algorithm to generate a hybrid task
    ############################################################
    # another way to generate a hybrid task
    # in this algo, we start from node 0 and edge 0-1
    # and there are 2 choices every step
    # we set 2 pointers, one for the current node, one for the latest node
    # 1. add an edge from current node to the latest node
    # e.g. current status: node set:(0,1) edge set (0->1),
    #       current node=0, latest node=1,
    #       then we add an new edge 0->2, and update the latest node to 2
    # 2. move current point to the next node
    # e.g. current status: node set:(0,1,2) edge set (0->1, 1->2),
    #       current node=0, latest node=2,
    #       then we move the current node to 1,
    #       do not add any edge, and do not update the latest node
    # the current node should never pass the latest node
    # we can choose either of the 2 choices randomly, and repeat the process
    # in this way, we can generate a hybrid task
    ############################################################


