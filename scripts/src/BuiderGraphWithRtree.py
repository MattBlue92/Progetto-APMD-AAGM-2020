import networkx as nx

from scripts.src.BuilderGraph import BuilderGraph
from rtree import index

class BuilderGraphWithRtree:
    def __init__(self, d, df):
        self.d=d
        self.df=df
        self.i=0
        self.rtree = index.Index()
        self.initialization()

    def initialization(self):
        self.df.apply(self.insert, axis=1)

    def insert(self, e):
        self.rtree.insert(self.i, (e["long"], e["lat"], e["long"], e["lat"]), obj=e["citta"])
        self.i=self.i+1

    def intersection(self):
        myDict = {}
        self.df.apply(lambda e: myDict.update(self.create_dictionary(e)), axis=1)
        return nx.Graph(myDict)


    def create_dictionary(self, e):
        myDict={}
        temp = list(self.rtree.intersection(
            (e["long"] - self.d, e["lat"] - self.d, e["long"] + self.d, e["lat"] + self.d), objects=True))
        myDict[e["citta"]] = [(item.object) for item in temp]
        return myDict
