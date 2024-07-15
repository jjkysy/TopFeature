from Feature_analyzer.features_analyses import FeatureAnalyse, FeatureEval
from Generator.graph_generator import GraphGen
from Plotter.fig_plotter import PlotGen

n_topologies = 100
n_nodes_in_topologies = 100
mas_topologies = ["hierarchical", "mesh", "chain", "pool", "star"]
task_topologies = ["linear", "parallel", "simple_hybrid", "layer_hybrid"]

storage_paths = {
    "topo_path": "stats/topo/",
    "topo_fea_path": "stats/feature/",
    "topo_plot_path": "plots/mas/",
    "task_plot_path": "plots/task/",
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

# step 3 calculating matching result
mas_feat_eval = FeatureEval(df_mas_features, storage_paths["topo_fea_path"])
df_mas_eval = mas_feat_eval.mas_eval()
task_feat_eval = FeatureEval(df_task_features, storage_paths["topo_fea_path"])
df_task_eval = task_feat_eval.task_eval()


# step 4 matching and optimizing


# along with step 1-4, do plotting and visualization
mas_plottor = PlotGen(
    df_mas_graph, df_mas_features, df_mas_eval, storage_paths["topo_plot_path"]
)
task_plottor = PlotGen(
    df_task_graph,
    df_task_features,
    df_task_eval,
    storage_paths["task_plot_path"],
)
# 1. plotting the graph
mas_plottor.plot_topo()
task_plottor.plot_topo()
# 2. plotting the graph features
mas_plottor.plot_feature()
task_plottor.plot_feature()
# 3. plotting the evaluation results
mas_plottor.plot_eval()
task_plottor.plot_eval()
