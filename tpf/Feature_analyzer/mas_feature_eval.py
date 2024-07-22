#################################################################
# in this file, we will evaluate the dependency and uncertainty
# of the MAS and task graphs
# we will combine the features of the graphs and evaluate the
# dependency and uncertainty


import numpy as np
from tpf.interface import GraphEval, GraphFeatures



class MASFeatureEvaluator:
    @classmethod
    def evaluate_dependency(cls, graph_feature: GraphFeatures) -> float:
        """
        Evaluate the dependency of the graph, using the features
        """
        dependency = (
            graph_feature.average_betweenness_centrality
            + (1 - graph_feature.average_closeness_centrality)
            + (1 - graph_feature.average_node_independence)
        ) / 3
        return dependency

    @classmethod
    def evaluate_uncertainty(cls, graph_feature: GraphFeatures) -> float:
        """
        Evaluate the uncertainty of the graph
        """
        feature_values = np.array(
            [
                graph_feature.average_betweenness_centrality,
                graph_feature.average_closeness_centrality,
                graph_feature.average_degree_centrality,
                graph_feature.average_node_independence,
                graph_feature.average_second_order_centrality,
                graph_feature.average_clustering_coefficient,
            ]
        )
        cvs = np.std(feature_values, ddof=1) / np.mean(feature_values)
        uncertainty = np.mean(cvs)
        return uncertainty

    @classmethod
    def evaluate_graph(cls, graph_feature: GraphFeatures) -> GraphEval:
        """
        Evaluate the graph
        """
        dependency = cls.evaluate_dependency(graph_feature)
        uncertainty = cls.evaluate_uncertainty(graph_feature)
        diameter = graph_feature.diameter
        g_evaluation = GraphEval(
            id=graph_feature.id,
            diameter=diameter,
            dependency=dependency,
            uncertainty=uncertainty,
        )
        return g_evaluation
