from typing import Dict

import networkx as nx
import numpy as np
from interface import GraphFeatures, GraphData


class AgentFeatures:
    @classmethod
    def calculate_node_independence(cls, graph: nx.DiGraph) -> Dict:
        n = len(graph)
        independence = {}
        max_distance = np.max(
            [
                d
                for u in graph
                for d in nx.single_source_shortest_path_length(
                    graph, u
                ).values()
            ]
        )
        for node in graph:
            total = sum(
                1
                - (nx.shortest_path_length(graph, node, target) / max_distance)
                for target in graph
                if node != target
            )
            independence[node] = total / (n - 1)
        return independence

    @classmethod
    def calculate_second_order_centrality(cls, graph: nx.DiGraph) -> Dict:
        soc = {}
        for node in graph:
            soc[node] = np.std(
                [
                    nx.shortest_path_length(graph, node, target)
                    for target in graph
                    if node != target
                ]
            )
        return soc

    @staticmethod
    def calculate_average_centrality(centrality_dict):
        return sum(centrality_dict.values()) / len(centrality_dict)

    @classmethod
    def calculate_features(cls, graph_data: GraphData) -> GraphFeatures:
        G = graph_data.graph
        degree_centrality = nx.degree_centrality(G)  # Degree centrality
        betweenness_centrality = nx.betweenness_centrality(
            G
        )  # Betweenness centrality
        closeness_centrality = nx.closeness_centrality(
            G
        )  # Closeness centrality
        edge_betweenness_centrality = nx.edge_betweenness_centrality(
            G
        )  # edge betweenness centrality
        eccentricity = nx.eccentricity(G)  # Eccentricity
        diameter = nx.diameter(G)
        radius = nx.radius(G)
        node_independence = cls.calculate_node_independence(
            G
        )  # node independence
        second_order_centrality = cls.calculate_second_order_centrality(
            G
        )  # second order centrality
        clustering_coefficient = nx.clustering(G)

        average_dc = cls.calculate_average_centrality(degree_centrality)
        average_bc = cls.calculate_average_centrality(betweenness_centrality)
        average_cc = cls.calculate_average_centrality(closeness_centrality)
        average_soc = cls.calculate_average_centrality(second_order_centrality)
        average_ni = cls.calculate_average_centrality(node_independence)
        average_clu_co = cls.calculate_average_centrality(
            clustering_coefficient
        )

        g_features = GraphFeatures(
            id=graph_data.id,
            degree_centrality=degree_centrality,
            betweenness_centrality=betweenness_centrality,
            closeness_centrality=closeness_centrality,
            edge_betweenness_centrality=edge_betweenness_centrality,
            eccentricity=eccentricity,
            diameter=diameter,
            radius=radius,
            node_independence=node_independence,
            second_order_centrality=second_order_centrality,
            clustering_coefficient=clustering_coefficient,
            average_betweenness_centrality=average_bc,
            average_closeness_centrality=average_cc,
            average_degree_centrality=average_dc,
            average_node_independence=average_ni,
            average_second_order_centrality=average_soc,
            average_clustering_coefficient=average_clu_co,
        )

        return g_features
