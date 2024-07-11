from Generator.graph_generator import GraphGen
from Feature_analyzer.features_analyses import FeatureAnalyse
from Plotter.fig_plotter import PlotGen

n_topologies = 100
n_nodes_in_topologies = 100
mas_topologies = ["hierarchical", "mesh", "chain", "pool", "star"]
task_topologies = ["linear", "parallel", "simple_hybrid", "layer_hybrid"]

storage_paths = {
    "topo_path": "stats/topo/",
    "topo_fea_path": "stats/feature/",
    "topo_plot_path": "plots/",
}

# step 1 generate graphs / or extract graphs (to be added)
mas_gen = GraphGen(storage_paths["topo_path"], "mas")
task_gen = GraphGen(storage_paths["topo_path"], "task")
df_mas_graph = mas_gen.gen_and_save_graph(
    mas_topologies, n_nodes_in_topologies, n_topologies
)
df_task_graph = task_gen.gen_and_save_graph(
    task_topologies, n_nodes_in_topologies, n_topologies
)

# step 2 analysing graph features
mas_feat_analyse = FeatureAnalyse(df_mas_graph, storage_paths["topo_fea_path"])
task_feat_analyse = FeatureAnalyse(
    df_task_graph, storage_paths["topo_fea_path"]
)
df_mas_features = mas_feat_analyse.mas_feature()
df_task_features = task_feat_analyse.task_feature()

# step 3 calculating matching result and optimizing

# step 4 plotting
mas_plottor = PlotGen(
    df_mas_graph, df_mas_features, storage_paths["topo_plot_path"]
)
mas_plottor.graph_plot()
mas_plottor.feature_plot()
task_plottor = PlotGen(
    df_task_graph, df_task_features, storage_paths["topo_plot_path"]
)
task_plottor.graph_plot()
task_plottor.feature_plot()
