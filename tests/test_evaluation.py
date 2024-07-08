import pytest
import networkx as nx
from tpf.evaluation import AgentFeatures
from tpf.interface import GraphData, GraphFeatures


@pytest.fixture
def mock_graph_data():
    G = nx.complete_graph(5)
    return GraphData(graph=nx.DiGraph(G), name="mock_graph")


@pytest.fixture
def mock_graph_features(mock_graph_data):
    return GraphFeatures(name=mock_graph_data.name)


def test_calculate_node_independence(mock_graph_data):
    independence = AgentFeatures.calculate_node_independence(
        mock_graph_data.graph
    )
    assert isinstance(independence, dict)
    assert all(
        isinstance(k, int) and isinstance(v, float)
        for k, v in independence.items()
    )


def test_calculate_second_order_centrality(mock_graph_data):
    soc = AgentFeatures.calculate_second_order_centrality(
        mock_graph_data.graph
    )
    assert isinstance(soc, dict)
    assert all(
        isinstance(k, int) and isinstance(v, float) for k, v in soc.items()
    )


def test_calculate_features(mock_graph_data):
    features = AgentFeatures.calculate_features([mock_graph_data])
    assert len(features) == 1
    assert isinstance(features[0], GraphFeatures)
    assert features[0].name == "mock_graph"


def test_features_values(mock_graph_features):
    feature_values = [
        mock_graph_features.degree_centrality,
        mock_graph_features.betweenness_centrality,
        mock_graph_features.closeness_centrality,
        mock_graph_features.edge_betweenness_centrality,
        mock_graph_features.eccentricity,
        mock_graph_features.node_independence,
        mock_graph_features.second_order_centrality,
        mock_graph_features.clustering_coefficient,
    ]
    for feature_value in feature_values:
        assert isinstance(feature_value, dict)
        assert all(
            isinstance(k, int) and (isinstance(v, float) or isinstance(v, int))
            for k, v in feature_value.items()
        )


def test_average_values(mock_graph_features):
    average_values = [
        mock_graph_features.average_betweenness_centrality,
        mock_graph_features.average_closeness_centrality,
        mock_graph_features.average_degree_centrality,
        mock_graph_features.average_node_independence,
        mock_graph_features.average_second_order_centrality,
        mock_graph_features.average_clustering_coefficient,
    ]
    for average_value in average_values:
        assert isinstance(average_value, float) or isinstance(
            average_value, int
        )
