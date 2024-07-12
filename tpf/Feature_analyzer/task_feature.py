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
        for i in range(max_degree + 1):
            for j in range(max_degree + 1):
                if joint_prob[i, j] > 0:
                    mutual_info += joint_prob[i, j] * np.log(
                        joint_prob[i, j]
                        / (marginal_prob_u[i] * marginal_prob_v[j])
                    )
        return mutual_info

    @classmethod
    def calculate_features(cls, graph_data: GraphData) -> TaskGraphFeatures:
        G = graph_data.graph
        entropy = cls.calculate_entropy(G)
        mutual_info = cls.calculate_mutual_information(G)
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
            information_entropy=entropy,
            mutual_information=mutual_info,
        )
        return t_features
