##############################################################################
# Randomly create agent topologies, every type 100, 100 node
# For now, we define the agent topologies as follows:
# Decentralized: meshes, chains, shared-pools
# Centralized: stars, hierarchicals (tree is a special case of hierarchical)
##############################################################################

from typing import List
import random

import networkx as nx
from interface import GraphData
import uuid


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
                    GraphData(
                        graph=directed_mesh,
                        name=f"mesh_{i}",
                        id=uuid.uuid4(),
                        type="mas",
                    )
                )
        return mesh_graph

    @classmethod
    def generate_chains(cls, n_node: int, n_graph: int) -> List[GraphData]:
        chain_graph = []
        for i in range(n_graph):
            chain = nx.path_graph(n_node)
            directed_chain = nx.DiGraph(chain)
            if nx.is_strongly_connected(directed_chain):
                chain_graph.append(
                    GraphData(
                        graph=directed_chain,
                        name=f"chain_{i}",
                        id=uuid.uuid4(),
                        type="mas",
                    )
                )
        return chain_graph

    @classmethod
    def generate_pools(cls, n_node: int, n_graph: int) -> List[GraphData]:
        # shared-pool is a star with a fully-connected sub grpah as center
        # we set the number of centers as 5%-30% of the total nodes
        pool_graph = []
        pool_nodes_num = random.choice(range(5, 30))
        for i in range(n_graph):
            pool = nx.complete_graph(pool_nodes_num, nx.DiGraph())
            for j in range(pool_nodes_num, n_node):
                center_node = random.choice(range(pool_nodes_num))
                pool.add_edge(j, center_node)
                pool.add_edge(center_node, j)
            if nx.is_strongly_connected(pool):
                pool_graph.append(
                    GraphData(
                        graph=pool,
                        name=f"pool_{i}",
                        id=uuid.uuid4(),
                        type="mas",
                    )
                )
        return pool_graph

    @classmethod
    def generate_stars(cls, n_node: int, n_graph: int) -> List[GraphData]:
        star_graph = []
        for i in range(n_graph):
            star = nx.star_graph(n_node - 1)
            directed_star = nx.DiGraph(star)
            if nx.is_strongly_connected(directed_star):
                star_graph.append(
                    GraphData(
                        graph=directed_star,
                        name=f"star_{i}",
                        id=uuid.uuid4(),
                        type="mas",
                    )
                )
        return star_graph

    @classmethod
    def generate_hierarchical(
        cls, n_node: int, n_graph: int
    ) -> List[GraphData]:
        # simplified as generated a random tree with n_node nodes
        hierarchical_graph = []
        for i in range(n_graph):
            hierarchical = nx.random_tree(n_node, create_using=nx.DiGraph())
            for edge in list(hierarchical.edges):
                hierarchical.add_edge(edge[1], edge[0])
            if nx.is_strongly_connected(hierarchical):
                hierarchical_graph.append(
                    GraphData(
                        graph=hierarchical,
                        name=f"hierarchical_{i}",
                        id=uuid.uuid4(),
                        type="mas",
                    )
                )
        return hierarchical_graph


# if __name__ == "__main__":
#     n_nodes_in_topologies = 100
#     n_topologies = 100
#     GeneratorFunction = Callable[[int, int], List[GraphData]]
#     generators: Dict[str, GeneratorFunction] = {
#         "mesh_test.pkl": AgentGraphGenerator.generate_meshes,
#         "chain_test.pkl": AgentGraphGenerator.generate_chains,
#         "pool_test.pkl": AgentGraphGenerator.generate_pools,
#         "star_test.pkl": AgentGraphGenerator.generate_stars,
#         "hierarchical_test.pkl": AgentGraphGenerator.generate_hierarchicals,
#     }
#     path = "topo/"
#     for filename, generator in generators.items():
#         with open(f"{path + filename}", "wb") as f:
#             pickle.dump(generator(n_nodes_in_topologies, n_topologies), f)
