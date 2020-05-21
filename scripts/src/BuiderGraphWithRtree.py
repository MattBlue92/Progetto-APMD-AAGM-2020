import networkx as nx

from scripts.src.BuilderGraph import BuilderGraph
from rtree import index

class BuilderGraphWithRtree:
    def __init__(self, d, long, lat, nameCities):
        self.d=d
        self.long=long
        self.lat=lat
        self.nameCities=nameCities
        self.rtree = index.Index()
        self.initialization()

    def initialization(self):
        for i in range(len(self.long)):
            self.rtree.insert(i, (self.long[i], self.lat[i], self.long[i], self.lat[i]), obj=self.nameCities[i])

    def intersection(self):
        myDict = {}
        for i in range(len(self.long)):
            temp = list(self.rtree.intersection((self.long[i] - self.d, self.lat[i] - self.d, self.long[i] + self.d, self.lat[i] + self.d), objects=True))
            myDict[self.nameCities[i]] = [(item.object) for item in temp]
        return nx.Graph(myDict)