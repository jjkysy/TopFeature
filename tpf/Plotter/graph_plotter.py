class GraphPlotter:
    def __init__(self, path: str):
        self.plot_storage = PlotStorage(path)
        self.layout_mapping = {
            "chain_0": nx.circular_layout,
            "mesh_0": nx.spring_layout,
            "pool_0": nx.spring_layout,
            "star_0": nx.spring_layout,
            "hierarchical_0": nx.spring_layout,
        }

    def plot_graph(self, graph: nx.DiGraph, name: str):
        plt.figure(figsize=(10, 10))
        layout_func = self.layout_mapping.get(name, nx.spring_layout)
        pos = layout_func(graph)
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_size=100,
            node_color="skyblue",
            font_size=8,
        )
        plt.title(name)
        self.plot_storage.save_plot(name)

    def plot_graphs(self, graphs: List[GraphData]):
        # only plot the first graph for now (100 in total)
        for graph_data in graphs[:1]:
            self.plot_graph(graph_data.graph, graph_data.name)