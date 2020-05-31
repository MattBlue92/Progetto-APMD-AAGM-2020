
from itertools import combinations
import networkx as nx

class CountingTriangles(object):

    def obviusAlgo(self, graph):
        triangles = {}
        for v in graph.nodes:
            nodes = list(graph.nodes)
            nodes.remove(v)
            couples = combinations(nodes, 2)
            t = 0
            for u,w in couples:
                if  graph.has_edge(v, u) and graph.has_edge(v,w) and graph.has_edge(u, w):
                    t = t + 1
            triangles[v] = t

        return triangles


    def algoEnum(self, graph):
        triangles = {}
        for v in graph.nodes():
            neighbors = list(graph[v])
            neighbors.remove(v)
            couples = combinations(neighbors, 2)
            t = 0
            for u, w in couples:
                if  graph.has_edge(v, u) and graph.has_edge(v, w) and graph.has_edge(u, w):
                    t = t + 1
            triangles[v] = t
        return triangles

    def lowDregree(self, graph):
        triangles = 0
        for v in graph.nodes():
            neighbors = list(filter(lambda x:  graph.degree(x)> graph.degree(v), list(graph[v])))
            couples = combinations(neighbors, 2)
            for u, w in couples:
                if  graph.has_edge(v, u) and graph.has_edge(v, w) and graph.has_edge(u, w):
                    triangles = triangles + 1

        return triangles


