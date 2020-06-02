
import networkx as nx
import numpy as np
import math
class ClosenessCentrality():

    def __init__(self):
        np.random.seed(42)

    def closenessUsingUtilities(self, graph, networkx=False):
        closeness = {}
        for v in graph.nodes():
            fv = 0
            count=0
            for w in graph.nodes():
                if nx.has_path(graph, v, w):
                    if v!=w:
                        path = nx.shortest_path(graph, v, w)
                        fv = fv + len(path)-1
                    count=count+1
            if fv!=0:
                if not networkx:
                    closeness[v]=(len(graph)-1)/fv
                else:
                    closeness[v] = (count-1)/fv
            else:
                closeness[v] = 0

        return closeness

    def closenessUsingBFS(self, graph, networkx=False):
        closeness = {}
        for v in graph.nodes():
            bfsTree = nx.bfs_tree(graph, v)
            fv = 0
            for w in bfsTree.nodes():
                fv = fv + self.distance(bfsTree, v, w)
            if fv!=0:
                if not networkx:
                    closeness[v] = (len(graph)-1)/fv
                else:
                    closeness[v] = (len(bfsTree) - 1) / fv
            else:
                closeness[v] = 0

        return closeness


    def distance(self, bfsTree, v, w):
        distance = 0
        bfsTree = bfsTree.reverse(copy = True)
        while v!=w:
            #neighbors = list(bfsTree[w])
            if w  in list(bfsTree.nodes()):
                neighbors = list(bfsTree[w])
                w = neighbors.pop()
                distance = distance+1
            else:
                break
        return  distance


    def closenessUsingEWAlgorithm(self, graph, epsilon):
        n = len(graph)
        k = int(math.log(n,10) / np.power(epsilon, 2))
        closeness = {}
        i = 0
        for u in graph.nodes():
            #bfsTree = nx.bfs_tree(graph, u)
            fv = 0
            #nodes = np.array(list(bfsTree.nodes()))
            nodes = np.random.choice(list(graph.nodes()), size= k, replace= False)
            #nodes= nodes[0]
            print("Iteration {} : {}".format(i,nodes))
            i = i+1
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
