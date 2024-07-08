import pickle
from typing import List
from agent_top import AgentGraphGenerator as Ag
from evaluation import AgentFeatures as Af
from fig_plot import (
    GraphPlotter,
    GraphFeaturesPlotter,
    TopoFeaturesPlotter,
)
import os


def save_file(file: List, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        return pickle.dump(file, f)


def load_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


n_topologies = 100
n_nodes_in_topologies = 100
topologies = ["hierarchicals", "meshes", "chains", "pools", "stars"]

generator_functions = {
    "hierarchicals": Ag.generate_hierarchicals,
    "meshes": Ag.generate_meshes,
    "chains": Ag.generate_chains,
    "pools": Ag.generate_pools,
    "stars": Ag.generate_stars,
}

storge_paths = {
    "topo_path": "stats/topo/",
    "topo_fea_path": "stats/topo_features/",
    "topo_plot_path": "plots/topo_plots/",
    "graph_fea_plot_path": "plots/graph_features_plots/",
    "topo_fea_plot_path": "plots/topo_features_plots/",
}


# generate topologies and save
for topo in topologies:
    topo_data = generator_functions[topo](n_nodes_in_topologies, n_topologies)
    save_file(topo_data, f"{storge_paths['topo_path']}{topo}_test.pkl")

    # calculate features and save
    topo_features = Af.calculate_features(topo_data)
    save_file(
        topo_features,
        f"{storge_paths['topo_fea_path']}{topo}_features.pkl",
    )

    # plot graphs and save
    Gp = GraphPlotter(storge_paths["topo_plot_path"])
    topo_plot = Gp.plot_graphs(topo_data)
    print(f"{topo.capitalize()} Graphs Plotted.")

    # plot features and save
    Gfp = GraphFeaturesPlotter(storge_paths["graph_fea_plot_path"])
    Gfp.plot_features_within_one_graph(topo_features)
    # Gfp.plot_size_features_for_topologies(topo_features, topo_fea_plot_path)
    print(f"{topo.capitalize()} Features Plotted.")
    print(f"{topo.capitalize()} Done.")
    print("-------------------------------------------------")
    # pass

# create a: features_dict: Dict[str, List[GraphFeatures]]
features_dict = {}
for topo in topologies:
    features = load_file(f"{storge_paths['topo_fea_path']}{topo}_features.pkl")
    features_dict[topo] = features
Tfp = TopoFeaturesPlotter(storge_paths["topo_fea_plot_path"])
Tfp.plot_size_and_centrality_for_topologies(features_dict)
Tfp.plot_centrality_features_for_topologies(features_dict)
