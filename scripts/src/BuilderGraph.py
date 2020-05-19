import networkx as nx

from scripts.src.Tools import Tools
import numpy as np

class BuilderGraph(object):

    def __init__(self, d):
        self.d = d
        #self.vertices = vertices
        self.tool = Tools()

    def buildGraph(self, df):
        if df is None:
            raise TypeError("Inputs are not not valide. long or lat is None. Please insert valid data!")

        numVertices = df.shape[0]
        matrixAdj = []
        cities = [tuple(city) for city in df[['long', 'lat']].to_numpy()]

        for cityA in cities:
            for cityB in cities:
                matrixAdj.append(self.tool.isConnected(cityA, cityB))

        matrixAdj = np.array(matrixAdj)
        matrixAdj = matrixAdj.reshape(numVertices, numVertices)

        graph = nx.from_numpy_array(matrixAdj)
        nameCities = df['citta'].values
        mapping = {}

        for i in np.arange(0, numVertices):
            mapping[i] = nameCities[i]

        return nx.relabel_nodes(graph, mapping)

