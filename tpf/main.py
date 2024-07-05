import pickle
from typing import List
from agent_top import AgentGraphGenerator as Ag
from evaluation import AgentFeatures as Af
from fig_plot import GraphPlotter as Gp
from fig_plot import GraphFeaturesPlotter as Gfp
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

# make "topo/" and "topo_fea/" defined paths
topo_path = "stat/topo/"
topo_fea_path = "stat/topo_fea/"
topo_plot_path = "plot/topo_plots/"
graph_fea_plot_path = "plot/graph_fea_plots/"
topo_fea_plot_path = "plot/topo_fea_plots/"


# generate topologies and save
for topo in topologies:
    topo_data = generator_functions[topo](n_nodes_in_topologies, n_topologies)
    save_file(topo_data, f"{topo_path}{topo}.pkl")

    # calculate features and save
    topo_features = Af.calculate_features(topo_data)
    save_file(topo_features, f"{topo_fea_path}{topo}_features.pkl")

    # plot graphs and save
    topo_plot = Gp.plot_graphs(topo_data, topo_plot_path)
    print(f"{topo.capitalize()} Graphs Plotted.")

    # plot features and save
    Gfp.plot_features_within_one_graph(topo_features, graph_fea_plot_path)
    # Gfp.plot_size_features_for_topologies(topo_features, topo_fea_plot_path)
    print(f"{topo.capitalize()} Features Plotted.")

    print(f"{topo.capitalize()} Done.")
    print("-------------------------------------------------")
    # pass

# create a: features_dict: Dict[str, List[GraphFeatures]]
features_dict = {}
for topo in topologies:
    features = load_file(f"{topo_fea_path}{topo}_features.pkl")
    features_dict[topo] = features
Gfp.plot_centrality_features_for_topologies(features_dict, topo_fea_plot_path)
Gfp.plot_size_and_centrality_for_topologies(features_dict, topo_fea_plot_path)
