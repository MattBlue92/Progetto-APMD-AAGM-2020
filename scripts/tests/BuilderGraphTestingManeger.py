import networkx as nx
import numpy as np
import pandas as pd

from scripts.src.Tools import Connections


class BuilderGraphTestingManeger:

    def __init__(self):
        self.tools = Connections(0.8)

    def expected_graph_creation(self, df):
        matrixAdj = []
        cities = [tuple(city) for city in df[['long', 'lat']].to_numpy()]
        for cityA in cities:
            for cityB in cities:
                matrixAdj.append(self.tools.isConnected(cityA, cityB))
        matrixAdj = np.array(matrixAdj)
        matrixAdj = matrixAdj.reshape(df.shape[0], df.shape[0])
        expectedGraph = nx.from_numpy_array(matrixAdj)
        expectedGraph.remove_edges_from(nx.selfloop_edges(expectedGraph))
        return expectedGraph

    def create_dataset_test(self):
        df = {'citta': ['Chieti', 'Acquila', 'Pescara', 'Teramo'],
              'lat': [42.351031167, 42.35122126, 42.46458398, 42.658918],
              'long': [14.167754574, 13.39843823, 14.2136422, 13.704439971]
              }
        df = pd.DataFrame(df)
        return df

    def createDisconnectedGraph(self):
        edges = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (3, 4), (3, 5), (4, 3), (4, 5), (5, 4), (5, 3)]
        graph = nx.Graph()
        graph.add_edges_from(edges)
        return graph
