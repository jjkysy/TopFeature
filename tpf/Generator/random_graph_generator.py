import uuid

import networkx as nx
import numpy as np
import pandas as pd
from interface import GraphData


class RandomGraphGenerator:
    def __init__(self, number_of_graphs):
        self.number_of_graphs = number_of_graphs

    def generate_BA_graph(self) -> pd.DataFrame:
        """
        generate a dataframe with columns: topology, data
        in which data is a GraphData object
        """
        G_list = []
        for _ in range(self.number_of_graphs):
            num_nodes = np.random.randint(50, 301)
            ba = nx.barabasi_albert_graph(num_nodes, 2)
            # 转换为有向图，并且每条边权重random在0-1之间
            ba = ba.to_directed()
            for edge in ba.edges:
                ba[edge[0]][edge[1]]["weight"] = np.random.rand()
            G_list.append(ba)
        df = pd.DataFrame(
            [
                {
                    "topology": "BA",
                    "data": GraphData(
                        graph=G, name=f"BA_{i}", id=uuid.uuid4(), type="task"
                    ),
                }
                for i, G in enumerate(G_list)
            ]
        )
        return df

    def generate_ER_graph(self) -> pd.DataFrame:
        """
        generate a dataframe with columns: topology, data
        in which data is a GraphData object
        """
        G_list = []
        for _ in range(self.number_of_graphs):
            num_nodes = np.random.randint(50, 301)
            er = nx.erdos_renyi_graph(num_nodes, 0.1)
            # 转换为有向图，并且每条边权重random在0-1之间
            er = er.to_directed()
            for edge in er.edges:
                er[edge[0]][edge[1]]["weight"] = np.random.rand()

            G_list.append(er)
        df = pd.DataFrame(
            [
                {
                    "topology": "ER",
                    "data": GraphData(
                        graph=G, name=f"ER_{i}", id=uuid.uuid4(), type="task"
                    ),
                }
                for i, G in enumerate(G_list)
            ]
        )
        return df

    def generate_WS_graph(self) -> pd.DataFrame:
        """
        generate a dataframe with columns: topology, data
        in which data is a GraphData object
        """
        G_list = []
        for _ in range(self.number_of_graphs):
            num_nodes = np.random.randint(50, 301)
            ws = nx.watts_strogatz_graph(num_nodes, 4, 0.1)
            # 转换为有向图，并且每条边权重random在0-1之间
            ws = ws.to_directed()
            for edge in ws.edges:
                ws[edge[0]][edge[1]]["weight"] = np.random.rand()

            G_list.append(ws)
        df = pd.DataFrame(
            [
                {
                    "topology": "WS",
                    "data": GraphData(
                        graph=G, name=f"WS_{i}", id=uuid.uuid4(), type="task"
                    ),
                }
                for i, G in enumerate(G_list)
            ]
        )
        return df

    # def generate_classical_graph(self, number_of_nodes) -> pd.DataFrame:
    #     """
    #     generate a dataframe with columns: topology, data
    #     in which data is a GraphData object
    #     """
    #     G_list = []
    #     for i in range(10, number_of_nodes + 10):
    #         linear = nx.DiGraph()
    #         for j in range(i - 1):
    #             # add random weight to the edge
    #             linear.add_edge(j, j + 1, weight=1)
    #         G_list.append(linear)
    #     for i in range(10, number_of_nodes + 10):
    #         parallel = nx.DiGraph()
    #         for j in range(1, i):
    #             parallel.add_edge(0, j, weight=1 / i - 1)
    #         G_list.append(parallel)

    #     half = len(G_list) // 2
    #     df = pd.DataFrame([
    #         {
    #             "topology": "linear",
    #             "data": GraphData(graph=G, name=f'linear_{i}',
    #                                id=uuid.uuid4(), type='task')
    #         }
    #         for i, G in enumerate(G_list[:half])
    #     ])
    #     df = pd.concat([df, pd.DataFrame([
    #         {
    #             "topology": "parallel",
    #             "data": GraphData(graph=G, name=f'parallel_{i}',
    #                               id=uuid.uuid4(), type='task')
    #         }
    #         for i, G in enumerate(G_list[half:])
    #     ])], ignore_index=True)
    #     return df
