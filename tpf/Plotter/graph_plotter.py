import networkx as nx
import matplotlib.pyplot as plt
from interface import GraphData
from utils import PlotStorage as PlotStorage


class GraphPlotter:
    layout_mapping = {
        "chain": nx.circular_layout,
        "mesh": nx.spring_layout,
        "pool": nx.spring_layout,
        "star": nx.spring_layout,
        "hierarchical": nx.spring_layout,
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
