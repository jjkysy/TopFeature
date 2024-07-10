from .Generator.graph_generator import GraphGen
from.Feature_analyzer.features_analyses import FeatureAnalyse
from tpf.Plotter.fig_plot import (
    GraphPlotter,
    GraphFeaturesPlotter,
    TopoFeaturesPlotter,
)

n_topologies = 100
n_nodes_in_topologies = 100
mas_topologies = ["hierarchical", "mesh", "chain", "pool", "star"]
task_topologies = ["linear", "parallel", "hierarchical"]

storage_paths = {
    "topo_path": "stats/topo/",
    "topo_fea_path": "stats/features/",
    "topo_plot_path": "plots/topo_plots/",
    "topo_fea_plot_path": "plots/topo_features_plots/"
}

# step 1 generate graphs / or extract graphs (to be added)
mas_gen = GraphGen(storage_paths["topo_path"], 'mas')
task_gen = GraphGen(storage_paths["topo_path"], 'task')
df_mas_graph = mas_gen.gen_and_save_graph(mas_topologies, n_nodes_in_topologies, n_topologies)
df_task_graph = task_gen.gen_and_save_graph(task_topologies, n_nodes_in_topologies, n_topologies)
# step 2 analysing graph features

mas_feat_analyse = FeatureAnalyse(df_mas_graph, storage_paths["topo_fea_path"])
task_feat_analyse = FeatureAnalyse(df_task_graph, storage_paths["topo_fea_path"])
df_mas_features = FeatureAnalyse.mas_feature

# step 3 calculating matching result and optimizing

# step 4 plotting


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


extractor()
graph_generator()
graph_analyse()
graph_optimizer()
graph_plotter()