import networkx as nx

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


    def intersection(self, flag=False):
        if flag:
            # weighted graph
            myDict = {obj[0]: self.createDict(obj)for obj in self.data}
            graph = nx.Graph(myDict)
#            nx.relabel_nodes(graph, mapping=self.mapping, copy= False)
            return graph
        else:
            myDict = {obj[0]:list(self.rtree.intersection((obj[1] - self.d, obj[2] - self.d, obj[1] + self.d, obj[2] + self.d))) for obj in self.data}
            graph = nx.Graph(myDict)
            nx.relabel_nodes(graph, mapping=self.mapping, copy= False)
            return graph

    def createDict(self, obj):
        temp=list(self.rtree.intersection((obj[1] - self.d, obj[2] - self.d, obj[1] + self.d, obj[2] + self.d)))
        myDict={}
        for elem_list in temp:
            myDict.update({self.mapping[elem_list]: {'weight':self.euclidean_distance(obj[0], elem_list)}})
        return myDict

    def euclidean_distance(self, obj, elem_list):
        from math import sqrt
        x_1=self.df[self.df["citta"]==obj].long.values[0]
        x_2=self.df[self.df["citta"] == obj].lat.values[0]
        y_1=self.df[self.df["citta"]==self.mapping[elem_list]].long.values[0]
        y_2=self.df[self.df["citta"] == self.mapping[elem_list]].lat.values[0]
        return sqrt((x_1-x_2)**2+(y_1-y_2)**2)
        #def createDict(self, obj):
    #    temp =  list(self.rtree.intersection((obj[1] - self.d, obj[2] - self.d, obj[1] + self.d, obj[2] + self.d),objects=True))
    #    myDict = {obj[0]:[(item.object) for item in temp]}
    #    print(myDict)
    #    return myDict
