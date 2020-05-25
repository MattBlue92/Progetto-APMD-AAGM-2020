import networkx as nx
import pandas as pd
import numpy as np

from scripts.src.BuilderGraph import BuilderGraph
from rtree import index

class BuilderGraphWithRtree:
    def __init__(self, d, df):
        self.d=d
        self.df=df
        self.data = [tuple(r) for r in df.to_numpy()]
        self.mapping = {}
        self.rtree = index.Index(self.generator_function())

    def generator_function(self):
        for i, obj in enumerate(self.data):
            self.mapping[i] =  obj[0]
            yield (i, (obj[1], obj[2], obj[1], obj[2]), obj[0])


    def buildGraph(self, flag=False):
        myDict = self.getNeighbors()
        if flag:
            # weighted graph
            # creation of adjacency verteces dataset
            dataset = self.prepareDatasetsForWeight(myDict)

            # compute the distances
            self.computeDistance(dataset)

            graph= nx.from_pandas_edgelist(dataset, "first_vertex", "second_vertex", ['weight'])
            return graph
        else:
            graph = nx.Graph(myDict)
            nx.relabel_nodes(graph, mapping=self.mapping, copy= False)
            return graph


        #def createDict(self, obj):

    def computeDistance(self, dataset):
        first_vertex = dataset.first_vertex.values
        second_vertex = dataset.second_vertex.values
        x_first = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].long.values[0], first_vertex)))
        y_first = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].lat.values[0], first_vertex)))
        x_second = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].long.values[0], second_vertex)))
        y_second = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].lat.values[0], second_vertex)))
        dataset["weight"] = np.sqrt(np.power(x_first - x_second, 2) + np.power(y_first - y_second, 2))

    def prepareDatasetsForWeight(self, myDict):
        dataset = pd.DataFrame.from_dict(myDict, orient="index").stack().to_frame()
        dataset.reset_index(inplace=True)
        dataset = dataset.drop(columns=["level_1"])
        dataset = dataset.rename(columns={"level_0": "first_vertex", 0: "second_vertex"})
        dataset.second_vertex = dataset.second_vertex.astype(int)
        second_vertex = dataset["second_vertex"].values
        dataset['second_vertex'] = np.array(list(map(lambda elem: self.mapping[elem], second_vertex)))
        return dataset

    def getNeighbors(self):
        """
        Tempo ese: O(nlogn) perchè abbiamo n vertici e per sapere il suo vicinaoto usamiamo la ricerca di RTree che costa O(logn)
        :return: ritorna un dizionario dove la chiave è un nodo e il valore è il suo vicinato
        """
        neighbors = {
            node[0]: list(self.rtree.intersection((node[1] - self.d, node[2] - self.d, node[1] + self.d, node[2] + self.d)))
            for node in self.data}
        return neighbors
    #    temp =  list(self.rtree.intersection((obj[1] - self.d, obj[2] - self.d, obj[1] + self.d, obj[2] + self.d),objects=True))
    #    myDict = {obj[0]:[(item.object) for item in temp]}
    #    print(myDict)
    #    return myDict
