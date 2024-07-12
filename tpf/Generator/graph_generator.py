from typing import Callable, Dict, List

import pandas as pd

from .agent_top import AgentGraphGenerator as Ag
from .task_top import TaskGraphGenerator as Tg


class GraphGen:
    def __init__(self, storage_path: str, g_type: str):
        GeneratorFunctionType = Callable[[int, int], List]
        self.generator_functions: Dict[
            str, Dict[str, GeneratorFunctionType]
        ] = {
            "task": {
                "linear": Tg.generate_linear_tasks,
                "parallel": Tg.generate_parallel_tasks,
                "simple_hybrid": Tg.generate_hybrid_tasks,
                "layer_hybrid": Tg.generate_layer_hybrid_tasks,
            },
            "mas": {
                "hierarchical": Ag.generate_hierarchical,
                "mesh": Ag.generate_meshes,
                "chain": Ag.generate_chains,
                "pool": Ag.generate_pools,
                "star": Ag.generate_stars,
            },
        }
        self.storage_path = storage_path
        self.type = g_type

    def gen_and_save_graph(
        self, topologies: List, n_nodes: int, n_graphs: int
    ) -> pd.DataFrame:
        topo_data_list = []

        for topo in topologies:
            if topo not in self.generator_functions[self.type]:
                print(f"Warning: {topo} generation function is not defined.")
                continue
            topo_data = self.generator_functions[self.type][topo](
                n_nodes, n_graphs
            )
            for data in topo_data:
                topo_data_list.append({"topology": topo, "data": data})

        #  save data to data frame
        df_graph = pd.DataFrame(topo_data_list)
        df_graph.to_pickle(f"{self.storage_path}{self.type}_data.pkl")
        return df_graph