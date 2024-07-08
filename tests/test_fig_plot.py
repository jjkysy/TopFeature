import pytest
from unittest.mock import patch
from tpf.fig_plot import (
    GraphPlotter,
    GraphFeaturesPlotter,
    TopoFeaturesPlotter,
)
from tpf.interface import GraphData, GraphFeatures
import networkx as nx


@pytest.fixture
def mock_graph_data():
    G = nx.complete_graph(5)
    return GraphData(graph=nx.DiGraph(G), name="mock_graph")


@pytest.fixture
def mock_graph_features():
    return GraphFeatures(name="mock_graph", diameter=5)


def test_plot_graph(mock_graph_data):
    with patch("tpf.fig_plot.PlotStorage.save_plot") as mock_save:
        plotter = GraphPlotter("mock_path")
        plotter.plot_graphs([mock_graph_data])
        mock_save.assert_called_once_with("mock_graph")


def test_plot_centrality_features(mock_graph_features):
    with patch("tpf.fig_plot.PlotStorage.save_plot") as mock_save:
        plotter = GraphFeaturesPlotter("mock_path")
        plotter.plot_features_within_one_graph([mock_graph_features])
        mock_save.assert_called_once_with("mock_graph_centrality")


def test_plot_size_features_for_topologies():
    mock_graph_features_list = [
        GraphFeatures(name=f"mock_graph_{i}", diameter=i) for i in range(10)
    ]
    with patch("tpf.fig_plot.PlotStorage.save_plot") as mock_save:
        plotter = TopoFeaturesPlotter("mock_path")
        plotter.plot_size_features_for_topologies(mock_graph_features_list)
        mock_save.assert_called_once_with("mock_graph_0_diameter")


def test_plot_centrality_features_for_topologies(mock_graph_features):
    with patch("tpf.fig_plot.PlotStorage.save_plot") as mock_save:
        plotter = TopoFeaturesPlotter("mock_path")
        plotter.plot_centrality_features_for_topologies(
            {"mock_graph": [mock_graph_features]}
        )
        mock_save.assert_called_once_with("average_centrality_comparison")


def test_plot_size_and_centrality_for_topologies(mock_graph_features):
    with patch("tpf.fig_plot.PlotStorage.save_plot") as mock_save:
        plotter = TopoFeaturesPlotter("mock_path")
        plotter.plot_size_and_centrality_for_topologies(
            {"mock_graph": [mock_graph_features]}
        )
        mock_save.assert_called_once_with("diameter_centrality")
