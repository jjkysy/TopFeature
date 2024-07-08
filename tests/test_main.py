import pytest
from unittest.mock import patch, MagicMock
import os
from main import save_file, load_file, generator_functions, storge_paths
from tpf.fig_plot import (
    GraphPlotter,
    GraphFeaturesPlotter,
    TopoFeaturesPlotter,
)


@pytest.fixture
def mock_data():
    return {"key": "value"}


def test_save_and_load_file(mock_data, tmpdir):
    filename = tmpdir.join("test.pkl")
    save_file(mock_data, filename)
    loaded_data = load_file(filename)
    assert mock_data == loaded_data


@pytest.mark.parametrize(
    "topo", ["hierarchicals", "meshes", "chains", "pools", "stars"]
)
def test_generator_functions(topo):
    with patch(
        f"tpf.agent_top.AgentGraphGenerator.{generator_functions[topo].__name__}",
        return_value=[],
    ):
        topo_data = generator_functions[topo](100, 100)
        assert isinstance(topo_data, list)


@patch("main.GraphPlotter.plot_graphs")
@patch("main.GraphFeaturesPlotter.plot_features_within_one_graph")
@patch("main.TopoFeaturesPlotter.plot_size_and_centrality_for_topologies")
@patch("main.TopoFeaturesPlotter.plot_centrality_features_for_topologies")
def test_main_flow(
    mock_plot_centrality,
    mock_plot_size,
    mock_plot_features,
    mock_plot_graphs,
    tmpdir,
):
    # Mock storage paths to use tmpdir
    mock_storge_paths = {
        "topo_path": tmpdir.join("stats/topo/"),
        "topo_fea_path": tmpdir.join("stats/topo_features/"),
        "topo_plot_path": tmpdir.join("plots/topo_plots/"),
        "graph_fea_plot_path": tmpdir.join("plots/graph_features_plots/"),
        "topo_fea_plot_path": tmpdir.join("plots/topo_features_plots/"),
    }

    for path in mock_storge_paths.values():
        os.makedirs(path, exist_ok=True)

    # Generate topologies
    for topo, generator in generator_functions.items():
        topo_data = generator(100, 100)
        save_file(
            topo_data, f"{mock_storge_paths['topo_path']}{topo}_test.pkl"
        )

        # Calculate features
        features = [{"name": f"{topo}_feature_{i}"} for i in range(100)]
        save_file(
            features,
            f"{mock_storge_paths['topo_fea_path']}{topo}_features.pkl",
        )

        # Plot graphs and features
        mock_plot_graphs.return_value = None
        mock_plot_features.return_value = None
        plotter = GraphPlotter(mock_storge_paths["topo_plot_path"])
        plotter.plot_graphs(topo_data)

        feature_plotter = GraphFeaturesPlotter(
            mock_storge_paths["graph_fea_plot_path"]
        )
        feature_plotter.plot_features_within_one_graph(features)

    # Create features_dict and plot size and centrality features
    features_dict = {
        topo: load_file(
            f"{mock_storge_paths['topo_fea_path']}{topo}_features.pkl"
        )
        for topo in generator_functions.keys()
    }
    Tfp = TopoFeaturesPlotter(mock_storge_paths["topo_fea_plot_path"])
    Tfp.plot_size_and_centrality_for_topologies(features_dict)
    Tfp.plot_centrality_features_for_topologies(features_dict)

    # Assert plot methods were called
    assert mock_plot_graphs.called
    assert mock_plot_features.called
    assert mock_plot_size.called
    assert mock_plot_centrality.called
