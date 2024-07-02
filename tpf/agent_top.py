# randomly create agent topologies, every type 100, 100 node

import pickle
from typing import List

import networkx as nx
from interface import GraphData


class AgentGraphGenerator:
    @classmethod
    def generate_trees(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        tree_graph = []
        for i in range(n_graph):
            tree = nx.gn_graph(n_node, create_using=nx.DiGraph)
            if nx.is_strongly_connected(tree):
                tree_graph.append(GraphData(graph=tree, name=f"tree_{i}"))
        return tree_graph

    @classmethod
    def generate_meshes(
        cls, n_node: int, n_graph: int, p=0.1, k=4
    ) -> List[GraphData]:
        mesh_graph = []
        for i in range(n_graph):
            mesh = nx.connected_watts_strogatz_graph(n_node, k, p, tries=100)
            directed_mesh = nx.DiGraph(mesh)
            if nx.is_strongly_connected(directed_mesh):
                mesh_graph.append(
                    GraphData(graph=directed_mesh, name=f"mesh_{i}")
                )
        return mesh_graph


if __name__ == "__main__":
    n_tree_nodes = 100
    n_mesh_nodes = 100
    n_trees = 100
    n_meshes = 100

    trees = AgentGraphGenerator.generate_trees(n_tree_nodes, n_trees)
    meshes = AgentGraphGenerator.generate_meshes(n_mesh_nodes, n_meshes)

    with open("tree_test.pkl", "wb") as f:
        pickle.dump(trees, f)

    with open("mesh_test.pkl", "wb") as f:
        pickle.dump(trees, f)
