import networkx as nx

from scripts.src.BuilderGraph import BuilderGraph
from rtree import index

class BuilderGraphWithRtree:
    def __init__(self, d, data):
        self.d=d
        self.data=data
        self.mapping = {}
        self.rtree = index.Index(self.generator_function())

    def generator_function(self):
        for i, obj in enumerate(self.data):
            self.mapping[i] =  obj[0]
            yield (i, (obj[1], obj[2], obj[1], obj[2]), obj[0])


    def intersection(self):
        myDict = {obj[0]:list(self.rtree.intersection((obj[1] - self.d, obj[2] - self.d, obj[1] + self.d, obj[2] + self.d))) for obj in self.data}
        graph = nx.Graph(myDict)
        nx.relabel_nodes(graph, mapping=self.mapping, copy= False)
        return graph


    #def createDict(self, obj):
    #    temp =  list(self.rtree.intersection((obj[1] - self.d, obj[2] - self.d, obj[1] + self.d, obj[2] + self.d),objects=True))
    #    myDict = {obj[0]:[(item.object) for item in temp]}
    #    print(myDict)
    #    return myDict