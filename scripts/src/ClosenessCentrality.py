
import networkx as nx
import numpy as np
import math
class ClosenessCentrality():

    def __init__(self):
        np.random.seed(42)

    def closenessUsingUtilities(self, graph):
        closeness = {}
        for v in graph.nodes():
            fv = 0
            for w in graph.nodes():
                if nx.has_path(graph, v, w) and v!=w:
                    pippo = nx.shortest_path(graph, v, w)
                    fv = fv + len(nx.shortest_path(graph, v, w))-1

            if fv!=0:
                closeness[v] = (len(graph)-1)/fv
            else:
                closeness[v] = 0

        return closeness

    def closenessUsingBFS(self, graph):
        closeness = {}
        for v in graph.nodes():
            bfsTree = nx.bfs_tree(graph, v)
            fv = 0
            for w in bfsTree.nodes():
                fv = fv + self.distance(bfsTree, v, w) #vs my version
            if fv!=0:
                closeness[v] = (len(graph)-1)/fv
            else:
                closeness[v] = 0

        return closeness


    def distance(self, bfsTree, v, w):
        distance = 0
        bfsTree = bfsTree.reverse(copy = True)
        while v!=w:
            neighbors = list(bfsTree[w])
            if len(neighbors)>0:
                w = neighbors.pop()
                distance = distance+1
            else:
                break
        return  distance


    def closenessUsingEWAlgorithm(self, graph, epsilon):
        n = len(graph)
        k = math.log(n,10) / np.power(epsilon, 2)
        closeness = {}
        for u in graph.nodes():
            #bfsTree = nx.bfs_tree(graph, u)
            fv = 0
            #nodes = np.array(list(bfsTree.nodes()))
            nodes = np.random.choice(list(graph.nodes()), size= int(k), replace= False)
            for w in nodes:
                bfsTree = nx.bfs_tree(graph, w)
                distance = self.distance(bfsTree, w, u)
                fv = fv+distance*(n/(k*(n-1)))

            if fv!=0:
                closeness[u] = 1/fv
            else:
                closeness[u] = 0

        return  closeness


    def armonicCloseness(self, graph):

        closeness ={}
        for v in graph.nodes():
            bfsTree = nx.bfs_tree(graph, v)
            fv = 0
            for w in bfsTree.nodes():
                distance = self.distance(bfsTree, v, w)
                if distance>0:
                    fv = fv + 1/distance #vs my version
            if fv!=0:
                closeness[v] = fv
            else:
                closeness[v] = 0

        return  closeness
