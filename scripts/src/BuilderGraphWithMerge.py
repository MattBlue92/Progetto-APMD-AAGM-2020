
import pandas as pd
import networkx as nx

from scripts.src.BuilderGraph import BuilderGraph

class BuilderGraphWithMerge(BuilderGraph):
    def __init__(self, d):
        super().__init__(d)

    def buildGraph(self, df):
        if df is None:
            raise TypeError("Inputs are not not valide. long or lat is None. Please insert valid data!")

        df["key"] = 1
        cartesian_product_df = pd.merge(df, df, on='key')
        cartesian_product_df = cartesian_product_df.drop("key", 1)

        columns = {"citta_x": "citta_1", "lat_x": "x", "long_x": "y", "citta_y": "citta_2", "lat_y": "z", "long_y": "w"}
        cartesian_product_df = cartesian_product_df.rename(columns=columns)

        cartesian_product_df["connections"] = cartesian_product_df.apply(self.tool.isConnectedFromRow, axis=1)

        connections = cartesian_product_df[cartesian_product_df["connections"] == True][
            ["citta_1", "citta_2"]]

        graph= nx.Graph()
        connections.apply(lambda e: graph.add_edge(e["citta_1"], e["citta_2"]), axis=1)
        return graph
