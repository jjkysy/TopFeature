#################################################################################
# Randomly create agent topologies, every type 100, 100 node
# For now, we define the agent topologies as follows:
# Decentralized: meshes, chains, shared-pools
# Centralized: stars, trees (can be regard as specific type of layered)
#################################################################################

import pickle
from typing import List
import random

import networkx as nx
from interface import GraphData


class AgentGraphGenerator:
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
    
    @classmethod
    def generate_chains(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        chain_graph = []
        for i in range(n_graph):
            chain = nx.path_graph(n_node)
            directed_chain = nx.DiGraph(chain)
            if nx.is_strongly_connected(directed_chain):
                chain_graph.append(
                    GraphData(graph=directed_chain, name=f"chain_{i}")
                )
        return chain_graph
    
    @classmethod
    def generate_pools(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        # shared-pool is a star with a fully-connected sub grpah as center
        # we set the number of centers as 5% of the total nodes
        pool_graph = []
        for i in range(n_graph):
            n_center = int(n_node * 0.05)
            pool = nx.complete_graph(n_center, nx.DiGraph())
            for j in range(n_center, n_node):
                center_node = random.choice(range(n_center))
                pool.add_edge(j, center_node)
                pool.add_edge(center_node, j)
            if nx.is_strongly_connected(pool):
                pool_graph.append(
                    GraphData(graph=pool, name=f"pool_{i}")
                )
        return pool_graph

    @classmethod
    def generate_stars(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        star_graph = []
        for i in range(n_graph):
            star = nx.star_graph(n_node-1) # since star_graph(n_node) has n_node+1 nodes
            directed_star = nx.DiGraph(star)
            if nx.is_strongly_connected(directed_star):
                star_graph.append(
                    GraphData(graph=directed_star, name=f"star_{i}")
                )
        return star_graph
    
    @classmethod
    def generate_trees(cls, n_node: int, n_graph: int) -> List[GraphData]:
        tree_graph = []
        for i in range(n_graph):
            tree = nx.gn_graph(n_node, create_using=nx.DiGraph)
            if nx.is_strongly_connected(tree):
                tree_graph.append(GraphData(graph=tree, name=f"tree_{i}"))
        return tree_graph

if __name__ == "__main__":
    n_nodes_in_topologies = 100
    n_topologies = 100
    generators = {
        "mesh_test.pkl": AgentGraphGenerator.generate_meshes,
        "chain_test.pkl": AgentGraphGenerator.generate_chains,
        "pool_test.pkl": AgentGraphGenerator.generate_pools,
        "star_test.pkl": AgentGraphGenerator.generate_stars,
        "tree_test.pkl": AgentGraphGenerator.generate_trees,
    }
    path = "topo/"
    for filename, generator in generators.items():
        with open(f"{path + filename}", "wb") as f:
            pickle.dump(generator(n_nodes_in_topologies, n_topologies), f)