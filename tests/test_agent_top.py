import pytest
from unittest.mock import patch, Mock
import networkx as nx
from tpf.agent_top import AgentGraphGenerator
from tpf.interface import GraphData


@pytest.fixture
def mock_graph_data():
    G = nx.complete_graph(5)
    return GraphData(graph=nx.DiGraph(G), name="mock_graph")


def test_generate_meshes(mock_graph_data):
    with patch(
        "tpf.agent_top.nx.connected_watts_strogatz_graph",
        return_value=mock_graph_data.graph,
    ):
        meshes = AgentGraphGenerator.generate_meshes(5, 1)
        assert len(meshes) == 1
        assert meshes[0].name == "mesh_0"
        assert isinstance(meshes[0].graph, nx.DiGraph)


def test_generate_chains(mock_graph_data):
    with patch(
        "tpf.agent_top.nx.path_graph", return_value=mock_graph_data.graph
    ):
        chains = AgentGraphGenerator.generate_chains(5, 1)
        assert len(chains) == 1
        assert chains[0].name == "chain_0"
        assert isinstance(chains[0].graph, nx.DiGraph)


def test_generate_pools(mock_graph_data):
    with patch(
        "tpf.agent_top.nx.complete_graph", return_value=mock_graph_data.graph
    ), patch("tpf.agent_top.random.choice", return_value=0):
        pools = AgentGraphGenerator.generate_pools(5, 1)
        assert len(pools) == 1
        assert pools[0].name == "pool_0"
        assert isinstance(pools[0].graph, nx.DiGraph)


def test_generate_stars(mock_graph_data):
    with patch(
        "tpf.agent_top.nx.star_graph", return_value=mock_graph_data.graph
    ):
        stars = AgentGraphGenerator.generate_stars(5, 1)
        assert len(stars) == 1
        assert stars[0].name == "star_0"
        assert isinstance(stars[0].graph, nx.DiGraph)


def test_generate_hierarchicals(mock_graph_data):
    with patch(
        "tpf.agent_top.nx.random_tree", return_value=mock_graph_data.graph
    ):
        hierarchicals = AgentGraphGenerator.generate_hierarchicals(5, 1)
        assert len(hierarchicals) == 1
        assert hierarchicals[0].name == "hierarchical_0"
        assert isinstance(hierarchicals[0].graph, nx.DiGraph)
