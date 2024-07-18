from typing import Dict

import networkx as nx
import numpy as np
from interface import GraphData, TaskGraphFeatures


class TaskFeatures:
    @classmethod
    def calculate_entropy(cls, graph: nx.DiGraph) -> float:
        degree = dict(graph.degree())
        n = len(graph)
        entropy = 0
        for d in degree.values():
            p = d / n
            entropy -= p * np.log(p)
        return entropy

    @classmethod
    def calculate_mutual_information(cls, graph: nx.DiGraph) -> float:
        degree = dict(graph.degree())
        degree_sequence = list(degree.values())
        max_degree = max(degree_sequence)
        joint_prob = np.zeros((max_degree + 1, max_degree + 1))
        for u, v in graph.edges():
            d_u = degree[u]
            d_v = degree[v]
            joint_prob[d_u, d_v] += 1
        joint_prob /= joint_prob.sum()
        marginal_prob_u = joint_prob.sum(axis=0)
        marginal_prob_v = joint_prob.sum(axis=1)
        mutual_info = 0
        epsilon = 1e-10
        for i in range(max_degree + 1):
            for j in range(max_degree + 1):
                if joint_prob[i, j] > 0:
                    mutual_info += joint_prob[i, j] * np.log(
                        joint_prob[i, j]
                        / (marginal_prob_u[i] * marginal_prob_v[j] + epsilon)
                    )
        return mutual_info

    @classmethod
    def calculate_path_length_entropy(cls, graph: nx.DiGraph) -> float:
        path_length_prob: Dict[int, float] = {}
        for node in range(len(graph)):
            if node == 0:
                continue
            else:
                paths = nx.all_simple_paths(graph, source=node, target=0)
                for path in paths:
                    path_length = len(path) - 1
                    prob = 1.0
                    for i in range(len(path) - 1):
                        prob *= graph[path[i]][path[i + 1]]["weight"]
                    if path_length in path_length_prob:
                        path_length_prob[path_length] += prob
                    else:
                        path_length_prob[path_length] = prob
        total_prob = sum(path_length_prob.values())
        for key in path_length_prob:
            path_length_prob[key] /= total_prob
        path_entropy = 0.0
        for prob in path_length_prob.values():
            path_entropy -= prob * np.log(prob)
        return path_entropy

    @classmethod
    def calculate_features(cls, graph_data: GraphData) -> TaskGraphFeatures:
        G = graph_data.graph
        entropy = cls.calculate_entropy(G)
        mutual_info = cls.calculate_mutual_information(G)
        path_length_entropy = cls.calculate_path_length_entropy(G)
        # calculate the sum of weight*indegree for each node
        weighted_sum_of_indegree = {}
        for node in G:
            weighted_sum_of_indegree[node] = sum(
                G[u][node]["weight"] for u in G.predecessors(node)
            )
        # overall SDI is the average of weighted_sum_of_indegree
        overall_SDI = sum(weighted_sum_of_indegree.values()) / len(
            weighted_sum_of_indegree
        )

        t_features = TaskGraphFeatures(
            id=graph_data.id,
            subtask_dependency_index=overall_SDI,
            node_degree_entropy=entropy,
            path_length_entropy=path_length_entropy,
            mutual_information=mutual_info,
        )
        return t_features
