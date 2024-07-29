#################################################################
# in this file, we will evaluate the dependency and uncertainty
# of the MAS and task graphs
# we will combine the features of the graphs and evaluate the
# dependency and uncertainty


import numpy as np
from interface import GraphEval, TaskGraphFeatures


class TaskFeatureEvaluator:
    @classmethod
    def evaluate_dependency(cls, task_feature: TaskGraphFeatures) -> float:
        """
        Evaluate the dependency of the graph, using the features
        """
        # combine SDI and mutual information
        feature_values = np.array(
            [
                task_feature.subtask_dependency_index,
                task_feature.mutual_information,
            ]
        )
        cvs = np.std(feature_values, ddof=1) / np.mean(feature_values)
        dependency = np.mean(cvs)
        return dependency

    @classmethod
    def evaluate_uncertainty(cls, task_feature: TaskGraphFeatures) -> float:
        """
        Evaluate the uncertainty of the graph
        """
        # TODO: consider entropy for now, may need more features
        # uncertainty = task_feature.node_degree_entropy
        uncertainty = task_feature.path_length_entropy
        return uncertainty

    @classmethod
    def evaluate_graph(cls, task_feature: TaskGraphFeatures) -> GraphEval:
        """
        Evaluate the graph
        """
        dependency = cls.evaluate_dependency(task_feature)
        uncertainty = cls.evaluate_uncertainty(task_feature)
        g_evaluation = GraphEval(
            id=task_feature.id,
            dependency=dependency,
            uncertainty=uncertainty,
        )
        return g_evaluation
