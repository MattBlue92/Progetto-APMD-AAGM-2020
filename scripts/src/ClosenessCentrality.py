
import networkx as nx
import numpy as np
import math


class CCAlgorithms():

    def distance_dict_bfs(self, graph, w):
        dist = {}
        queue = [w]
        marked = [w]
        dist[w] = 0
        while len(queue) > 0:
            v = queue.pop(0)
            for u in graph[v]:
                if not u in marked:
                    marked.append(u)
                    queue.append(u)
                    dist[u] = dist[v] + 1
        return dist


class ClosenessCentralityBFS(CCAlgorithms):

    def run(self, graph):
        closeness = {}
        nodes = graph.nodes._nodes
        len_nodes = len(nodes)
        for v in nodes:
            fv = sum(self.distance_dict_bfs(graph,v).values())
            closeness[v] = (len_nodes-1)/fv
        return closeness

class EWAlgorithm(CCAlgorithms):
    def __init__(self, graph, epsilon):
        super().__init__()
        self.graph = graph
        self.nodes = graph.nodes._nodes
        self.numNodes = len(self.nodes)
        self.k = math.floor(math.log(self.numNodes, 10) / np.power(epsilon, 2))
        self.alpha = self.numNodes / (self.k * (self.numNodes - 1))
        np.random.seed(48)
        if self.k<self.numNodes:
            self.sample_nodes = np.random.choice(list(self.nodes), size=self.k, replace=False)
        else:
            raise ValueError("Con k = {} Non si può costruire un campione più grande del numero di nodi presenti nel grafo".format(self.k))

    def run(self):
        closeness = {}
        dict_distance = dict(map(lambda w: (w, self.distance_dict_bfs(self.graph, w)), self.sample_nodes))
        for u in self.nodes:
            fv = 0
            for w in self.sample_nodes:
                fv = fv+dict_distance[w][u]*self.alpha
            closeness[u] = 1/fv
        return closeness
