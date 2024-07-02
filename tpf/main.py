import pickle
from typing import List

from agent_top import AgentGraphGenerator as Ag
from evaluation import AgentFeatures as Af


def save_file(file: List, filename):
    with open(filename, "wb") as f:
        return pickle.dump(file, f)


def load_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def analyze_features(features):
    # to be replaced by plotting, not printing
    for feature_set in features:
        print(f"Graph Name: {feature_set.name}")
        print("Degree Centrality: ", feature_set.degree_centrality)
        print("Betweenness Centrality: ", feature_set.betweenness_centrality)
        print("Closeness Centrality: ", feature_set.closeness_centrality)
        print(
            "Edge Betweenness Centrality: ",
            feature_set.edge_betweenness_centrality,
        )
        print("Eccentricity: ", feature_set.eccentricity)
        print("Diameter: ", feature_set.diameter)
        print("Radius: ", feature_set.radius)
        print("Node Independence: ", feature_set.node_independence)
        print("Second Order Centrality: ", feature_set.second_order_centrality)
        print("Clustering Coefficient: ", feature_set.clustering_coefficient)
        print("\n")


n_tree_nodes = 100
n_mesh_nodes = 100
n_trees = 100
n_meshes = 100

trees = Ag.generate_trees(n_tree_nodes, n_trees)
meshes = Ag.generate_meshes(n_mesh_nodes, n_meshes)

save_file(trees, "trees.pkl")
save_file(meshes, "meshes.pkl")

trees = load_file("trees.pkl")
meshes = load_file("meshes.pkl")

tree_features = Af.calculate_features(trees)
mesh_features = Af.calculate_features(meshes)

save_file(tree_features, "tree_features.pkl")
save_file(mesh_features, "mesh_features.pkl")

tree_features = load_file("tree_features.pkl")
mesh_features = load_file("mesh_features.pkl")


print("Tree Features Analysis:")
analyze_features(tree_features)

print("Mesh Features Analysis:")
analyze_features(mesh_features)
