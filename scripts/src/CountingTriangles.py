
from itertools import combinations
import networkx as nx

class CountingTriangles(object):
    def __init__(self):
        self.iterations=0

    def run(self,graph):
        pass

    def countTrianglesFromCouples(self, couples, graph, v):
        triangles = 0
        for u, w in couples:
            self.iterations=self.iterations+1
            if graph.has_edge(v, u) and graph.has_edge(v, w) and graph.has_edge(u, w):
                triangles = triangles + 1
        return triangles

    def get_iterations(self):
        return self.iterations

class ObviousAlgorithm(CountingTriangles):
    def run(self, graph):
        triangles = {}
        nodes = graph.nodes._nodes
        for v in nodes:
            self.iterations = self.iterations + 1
            nodes_list = list(nodes)
            if v in nodes_list:
                nodes_list.remove(v)
            couples = combinations(nodes_list, 2)
            t = self.countTrianglesFromCouples(couples, graph, v)
            triangles[v] = t

        return triangles

class EnumeratingNeighborPairs(CountingTriangles):
    def run(self, graph):
        triangles = {}
        nodes = graph.nodes._nodes
        for v in nodes:
            self.iterations = self.iterations + 1
            neighbors = list(graph[v])
            if v in neighbors:
                neighbors.remove(v)
            couples = combinations(neighbors, 2)
            t = self.countTrianglesFromCouples(couples, graph, v)
            triangles[v] = t
        return triangles

class DelegatingLowDegreeVertices(CountingTriangles):
    def run(self, graph):
        triangles = 0
        nodes=graph.nodes._nodes
        for v in nodes:
            neighbors = list(filter(lambda x:  graph.degree(x)> graph.degree(v) or (graph.degree(x)==graph.degree(v) and x>v), list(graph[v])))
            couples = combinations(neighbors, 2)
            triangles=triangles+self.countTrianglesFromCouples(couples, graph, v)
            self.iterations=self.iterations+1
        return triangles


