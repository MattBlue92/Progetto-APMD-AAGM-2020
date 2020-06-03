
from itertools import combinations
import networkx as nx

class CountingTriangles(object):
    def run(self,graph):
        pass

    def countTrianglesFromCouples(self, couples, graph, v):
        triangles = 0
        for u, w in couples:
            if graph.has_edge(v, u) and graph.has_edge(v, w) and graph.has_edge(u, w):
                triangles = triangles + 1
        return triangles

class ObviousAlgorithm(CountingTriangles):
    def run(self, graph):
        triangles = {}
        nodes = graph.nodes._nodes
        for v in nodes:
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
        return triangles


