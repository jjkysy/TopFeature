#################################################################
# in this file, we will evaluate the dependency and uncertainty
# of the MAS and task graphs
# we will combine the features of the graphs and evaluate the
# dependency and uncertainty


import numpy as np
from interface import GraphEval, GraphFeatures
from sklearn.preprocessing import MinMaxScaler


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
        ).reshape(1, -1)

        scaler = MinMaxScaler()
        normalized_features = scaler.fit_transform(feature_values)
        uncertainty = np.std(normalized_features)
        return uncertainty

    @classmethod
    def evaluate_graph(cls, graph_feature: GraphFeatures) -> GraphEval:
        """
        Evaluate the graph
        """
        dependency = cls.evaluate_dependency(graph_feature)
        uncertainty = cls.evaluate_uncertainty(graph_feature)
        g_evaluation = GraphEval(
            id=graph_feature.id,
            dependency=dependency,
            uncertainty=uncertainty,
        )
        return g_evaluation
