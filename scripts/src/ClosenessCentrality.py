
import networkx as nx
import numpy as np
import math
class ClosenessCentrality():

    def __init__(self):
        np.random.seed(47)

    def closenessUsingBFS(self, graph, networkx=False):
        closeness = {}
        nodes=graph.nodes._nodes
        len_nodes=len(nodes)
        for v in nodes:
            bfsTree = nx.bfs_tree(graph, v)
            bfs_nodes = bfsTree.nodes._nodes
            len_bfs_nodes = len(bfs_nodes)
            fv = 0
            for w in bfs_nodes:
                fv = fv + self.distance(bfsTree, v, w)
            if fv!=0:
                if not networkx:
                    closeness[v] = (len_nodes-1)/fv
                else:
                    closeness[v] = (len_bfs_nodes - 1) / fv
            else:
                closeness[v] = 0

        return closeness


    def closenessUsingEWAlgorithm(self ,graph, epsilon, c):
        # we suppose that graph is a connected component
        n = len(graph)
        k = math.floor(math.log(n, 10) / np.power(epsilon, 2))*c
        nodes = graph.nodes._nodes
        closeness = {}

        sample_nodes = np.random.choice(list(nodes), size=k, replace=False)
        dict_distance = {w:self.distance_dict_bfs(graph,w) for w in sample_nodes}

        for u in nodes:
            fv = 0
            for w in sample_nodes:
                fv = fv + dict_distance[w][u]*(n / (k*(n - 1)))
            closeness[u] = 1/fv


        return closeness

    def distance_dict_bfs(self, graph, w):
        # return the dict {(u,v): d(u,v), v in V e w in S}
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


    def distance(self, bfsTree, v, w):
        distance = 0
        bfsTree = bfsTree.reverse(copy = True)
        while v!=w:
            bfsTreeNodes=bfsTree.nodes._nodes
            if w  in bfsTreeNodes:
                neighbors = list(bfsTree[w])
                w = neighbors.pop()
                distance = distance+1
            else:
                break
        return  distance