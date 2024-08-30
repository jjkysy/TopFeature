import logging
import random
import uuid

# import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from Feature_analyzer.features_analyses import FeatureAnalyse, FeatureEval
from Generator.random_graph_generator import RandomGraphGenerator
from interface import GraphData
from Plotter.fig_plotter import PlotGen

logging.basicConfig(level=logging.INFO)

random_gen = RandomGraphGenerator(300)

file_path = "stats/omega_matrix/"
save_path = "stats/pruned_matrix/"
file_names = [
    ("omega_matrix_0.005_50.npy", "pruned_50"),
    ("omega_matrix_0.005_100.npy", "pruned_100"),
    ("omega_matrix_0.005_200.npy", "pruned_200"),
    ("omega_matrix_0.005_300.npy", "pruned_300"),
]


def prune_adjacency_matrix(adjacency_matrix, record_probability=0.1):
    """
    Paras:
        adjacency_matrix (np.ndarray)
        record_probability (float)
    Returns:
        adjacency_matrix (np.ndarray)
        step_matrices (list)
    """
    num_nodes = adjacency_matrix.shape[0]
    prune_count = 0
    pruned_matrix = adjacency_matrix.copy()
    step_matrices = []
    step_matrices.append(adjacency_matrix)

    for A in range(num_nodes):
        for C in range(num_nodes):
            if A != C:
                for B in range(num_nodes):
                    if A != B and B != C:
                        if (
                            adjacency_matrix[A, B] + adjacency_matrix[B, C]
                            < adjacency_matrix[A, C]
                        ):
                            if pruned_matrix[A, B] != 0:
                                pruned_matrix[A, B] = 0
                                prune_count += 1
                            if pruned_matrix[B, C] != 0:
                                pruned_matrix[B, C] = 0
                                prune_count += 1
                            if random.random() < record_probability:
                                step_matrices.append(pruned_matrix.copy())

    # only keep some steps, uniformly sampled
    num_to_keep = int(record_probability * 3000)
    if len(step_matrices) > num_to_keep:
        step_matrices = [
            step_matrices[i]
            for i in range(
                0, len(step_matrices), len(step_matrices) // num_to_keep
            )
        ]

    logging.info(f"Successful Prune count: {prune_count}")
    edges_remain_num = np.count_nonzero(pruned_matrix)
    logging.info(f"Edges remain: {edges_remain_num}")
    step_matrices.append(pruned_matrix)
    np.save(save_path + "pruned_" + str(num_nodes) + ".npy", pruned_matrix)
    logging.info(f"Pruned matrix saved at {save_path}pruned_{num_nodes}.npy")
    return step_matrices


def process_matrices(file_names, file_path):
    G_list_dict = {}
    for file_name in file_names:
        real_matrix = np.load(file_path + file_name)
        step_matrices = prune_adjacency_matrix(real_matrix)
        G_list = [
            nx.from_numpy_array(matrix, create_using=nx.DiGraph)
            for matrix in step_matrices
        ]
        G_list_dict[file_name] = G_list

    return G_list_dict


# assert not a fully connected graph
def is_fully_connected(graph):
    nodes = list(graph.nodes())
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                if not graph.has_edge(nodes[i], nodes[j]):
                    return False
    return True


# main function
# step 1 generate graphs / or extract graphs (to be added)
G_list_dict = process_matrices([name for name, _ in file_names], file_path)
for i in range(1, len(G_list_dict["omega_matrix_0.005_50.npy"])):
    assert not is_fully_connected(G_list_dict["omega_matrix_0.005_50.npy"][i])

# df_classical = generate_classical_graph(300)
df_comparison = pd.concat(
    [
        random_gen.generate_ER_graph(),
        random_gen.generate_WS_graph(),
        random_gen.generate_BA_graph(),
    ],
    ignore_index=True,
)

df_graph = pd.DataFrame(
    [
        {
            "topology": topology,
            "data": GraphData(
                graph=G, name=f"{topology}_{i}", id=uuid.uuid4(), type="task"
            ),
        }
        for file_name, topology in file_names
        for i, G in enumerate(G_list_dict[file_name])
    ]
)
df_graph = pd.concat([df_graph, df_comparison], ignore_index=True)

logging.info(
    f"Graphs number for each topology: {df_graph['topology'].value_counts()}"
)

# step 2 analysing graph features
feat_analyse = FeatureAnalyse(df_graph, "stats/feature/")
df_features = feat_analyse.task_feature()

# step 3 calculating matching result
feat_eval = FeatureEval(df_features, "stats/feature/")
df_eval = feat_eval.task_eval()

# step 4 matching and optimizing

# along with step 1-4, do plotting and visualization
plottor = PlotGen(df_graph, df_features, df_eval, "plots/pruned_graph/")
# 1. plotting the graph
# plottor.plot_topo()
# 2. plotting the graph features
plottor.plot_feature()
# 3. plotting the graph evaluation
plottor.plot_eval()
