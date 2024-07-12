import matplotlib.pyplot as plt
import networkx as nx
from interface import GraphData
from utils import PlotStorage as PlotStorage


class GraphPlotter:
    layout_mapping = {
        "chain_0": nx.circular_layout,
        "linear_0": nx.circular_layout,
        "mesh_0": nx.spring_layout,
        "pool_0": nx.spring_layout,
        "star_0": nx.spring_layout,
        "hierarchical_0": nx.spring_layout,
    }

    @classmethod
    def plot_graph(cls, graph_data: GraphData, storage_path: str):
        plt.figure(figsize=(10, 10))
        layout_func = cls.layout_mapping.get(graph_data.name, nx.spring_layout)
        pos = layout_func(graph_data.graph)
        nx.draw(
            graph_data.graph,
            pos,
            with_labels=True,
            node_size=100,
            node_color="skyblue",
            font_size=8,
        )
        plt.title(graph_data.name)
        plot_storage = PlotStorage(storage_path)
        plot_storage.save_plot(graph_data.name)
