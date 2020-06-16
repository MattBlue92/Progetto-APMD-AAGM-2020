########################################################################################################################
############################ CORSO DI LAUREA MAGISTRALE IN INFORMATICA #################################################
############################         Curriculum Data Science           #################################################
#             Matteo Ghera       matteo.ghera@stud.unifi.it
#             Matteo Marulli     matteo.marulli@stud.unifi.it
#######################################################################################################################

#run instruction:
#
#runfile('E:/Documenti/Magistrale/PycharmProject/Progetto-APMD-AAGM-2020/ghera-marulli.py', wdir='E:/Documenti/Magistrale/PycharmProject/Progetto-APMD-AAGM-2020')

# BuilderGraphWithRtree.py


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


    def buildGraph(self, flag=False):
        myDict = self.getNeighbors()
        if flag:
            # weighted graph
            # creation of adjacency verteces dataset
            dataset = self.prepareDatasetsForWeight(myDict)

            # compute the distances
            self.computeDistance(dataset)

            graph= nx.from_pandas_edgelist(dataset, "first_vertex", "second_vertex", ['weight'])
            graph.remove_edges_from(nx.selfloop_edges(graph))
            return graph
        else:
            graph = nx.Graph(myDict)
            nx.relabel_nodes(graph, mapping=self.mapping, copy= False)
            graph.remove_edges_from(nx.selfloop_edges(graph))
            return graph



    def computeDistance(self, dataset):
        first_vertex = dataset.first_vertex.values
        second_vertex = dataset.second_vertex.values
        x_first = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].long.values[0], first_vertex)))
        y_first = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].lat.values[0], first_vertex)))
        x_second = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].long.values[0], second_vertex)))
        y_second = np.array(list(map(lambda elem: self.df[self.df["citta"] == elem].lat.values[0], second_vertex)))
        dataset["weight"] = np.sqrt(np.power(x_first - x_second, 2) + np.power(y_first - y_second, 2))

    def prepareDatasetsForWeight(self, myDict):
        dataset = pd.DataFrame.from_dict(myDict, orient="index").stack().to_frame()
        dataset.reset_index(inplace=True)
        dataset = dataset.drop(columns=["level_1"])
        dataset = dataset.rename(columns={"level_0": "first_vertex", 0: "second_vertex"})
        dataset.second_vertex = dataset.second_vertex.astype(int)
        second_vertex = dataset["second_vertex"].values
        dataset['second_vertex'] = np.array(list(map(lambda elem: self.mapping[elem], second_vertex)))
        return dataset

    def getNeighbors(self):
        """
        Tempo ese: O(nlogn) perchè abbiamo n vertici e per sapere il suo vicinaoto usamiamo la ricerca di RTree che costa O(logn)
        :return: ritorna un dizionario dove la chiave è un nodo e il valore è il suo vicinato
        """
        neighbors = {
            node[0]: list(self.rtree.intersection((node[1] - self.d, node[2] - self.d, node[1] + self.d, node[2] + self.d)))
            for node in self.data}
        return neighbors



# ClosenessCentrality.py

import numpy as np
import math
class ClosenessCentralityBFS():

    def run(self, graph, networkx=False):
        #We suppose that  graph is a maximal connected component. (isolated nodes aren't allow )
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

            if not networkx:
                closeness[v] = (len_nodes-1)/fv
            else:
                closeness[v] = (len_bfs_nodes - 1) / fv


        return closeness

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


class EWAlgorithm:
    def __init__(self, graph, epsilon):
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

    def distance_dict_bfs(self, graph, w):
        # return the dict {v: d(v,w), v in V}
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


# CountingTriangles.py

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


#################### Notebooks

# # Building the graph

# In[1]:


from IPython import get_ipython
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)


# In[2]:


def makeUpGraph(graph, df, columns, node_size):
    pos = {}
    df.apply(lambda e: pos.update({e[columns[0]]: (e[columns[1]], e[columns[2]])}), axis=1)
    nx.draw(graph, pos, with_labels=True, node_size=node_size, alpha=0.55, cmap=plt.cm.RdPu,
            node_color=np.arange(graph.number_of_nodes()))


def statisticsOfGraph(graph):
    number_of_nodes = len(graph)
    number_of_edges = graph.number_of_edges()
    density = (2 * number_of_edges) / (number_of_nodes * (number_of_nodes - 1))

    return "STATISTICS: \nnumber of node:\t\t" + str(number_of_nodes) + "\nnumber of edges:\t" + str(
        number_of_edges) + "\ndensity:\t\t" + str(round(density, 4))


# In[3]:


import os
from path import Path

PROJ_DIR = Path().getcwd()
DATA_DIR = PROJ_DIR / "data"
os.chdir(PROJ_DIR)

# In[4]:


#from scripts.src.BuilderGraphWithRtree import BuilderGraphWithRtree

# ## Cities graph

# In[5]:


import json

with open(DATA_DIR / 'dpc-covid19-ita-province.json') as f:
    d = json.load(f)
json.dumps(d)
covid19_dataset = pd.DataFrame(d)

# In[6]:


covid19_dataset.drop_duplicates(subset=['denominazione_provincia'], inplace=True)
covid19_dataset = covid19_dataset[covid19_dataset != "In fase di definizione/aggiornamento"]
covid19_dataset = covid19_dataset.dropna()
provincia = covid19_dataset['denominazione_provincia']
lat = covid19_dataset['lat']
long = covid19_dataset['long']
province = pd.DataFrame(data={'citta': provincia, 'lat': lat, 'long': long})
province.head()

# In[7]:


d_provincia = 0.8
d_random = 0.8

# In[8]:


builderGraph4 = BuilderGraphWithRtree(d_provincia, province.copy())
P = builderGraph4.buildGraph()

# In[9]:


print(statisticsOfGraph(P))

# In[10]:


plt.figure(figsize=(22, 20), dpi=150)
makeUpGraph(P, province, ['citta', 'long', 'lat'], 5000)
plt.show()

# In[11]:


get_ipython().run_line_magic('timeit', 'builderGraph4.buildGraph()')

# ## Random Dataset

# In[12]:


data = np.random.uniform([30, 10], [50, 20], size=(2000, 2))
id = np.array([np.arange(2000)])
data = np.hstack([id.T, data])
data = pd.DataFrame(data, columns=["citta", "long", "lat"])
data.citta = data.citta.astype('int32')
data.citta = data.citta.astype('str')
data.head()

# In[13]:


builderGraph4 = BuilderGraphWithRtree(d_random, data.copy())
R = builderGraph4.buildGraph()

# In[14]:


print(statisticsOfGraph(R))

# In[15]:


get_ipython().run_line_magic('timeit', 'builderGraph4.buildGraph()')

# ## Weighted graphs

# In[16]:


builderGraph4 = BuilderGraphWithRtree(d_provincia, province.copy())
P_weight = builderGraph4.buildGraph(flag=True)

# In[17]:


builderGraph4 = BuilderGraphWithRtree(d_random, data.copy())
R_weight = builderGraph4.buildGraph(flag=True)

# In[18]:


nx.write_adjlist(P, DATA_DIR / "P.adjlist", delimiter=",")
nx.write_weighted_edgelist(P_weight, DATA_DIR / "P_weight.edgelist", delimiter=",")
nx.write_adjlist(R, DATA_DIR / "R.adjlist", delimiter=",")
nx.write_weighted_edgelist(R_weight, DATA_DIR / "R_weight.edgelist", delimiter=",")


# # Closeness Centrality

# In[1]:


def checkAsymptoticConvergence(expected, actual, epsilon, d):
    result = True
    for key in actual.keys():
        c_hat=1/actual[key]
        c=1/expected[key]
        abs_error = abs(c_hat - c)
        if abs_error>epsilon*d:
            print("actual: {}, expected: {}, error: {}".format(c_hat, c, abs_error))
        result = result and abs_error< epsilon*d
    return result


# In[2]:


#import os
#import networkx as nx
#from path import Path
#PROJ_DIR = Path().getcwd().parent
#DATA_DIR = PROJ_DIR / "data"
#os.chdir (PROJ_DIR)


# In[3]:


#from scripts.src.ClosenessCentrality import ClosenessCentralityBFS, EWAlgorithm


# In[4]:


# import networks
P=nx.read_adjlist(DATA_DIR/"P.adjlist", delimiter=",")
R=nx.read_adjlist(DATA_DIR/"R.adjlist", delimiter=",")


# ## P network

# In[5]:


largest_cc = max(nx.connected_components(P), key=len)
P=P.subgraph(largest_cc)
expected = nx.closeness_centrality(P, wf_improved=False)


# In[6]:


cc = ClosenessCentralityBFS()
actual = cc.run(P, networkx=True)
assert expected == actual


# In[7]:


print("Expected: {} \n Actual: {}".format(expected, actual))


# In[8]:


epsilon=0.165
EW = EWAlgorithm(P,epsilon)
expected = nx.closeness_centrality(P, wf_improved=False)
actual = EW.run()
diameter = nx.diameter(P)
assert checkAsymptoticConvergence(actual, expected, epsilon, diameter)


# In[9]:


get_ipython().run_line_magic('timeit', 'cc.run(P, networkx=True)')


# In[10]:


get_ipython().run_line_magic('timeit', 'EW.run()')


# ## R network

# In[11]:


largest_cc = max(nx.connected_components(R), key=len)
R=R.subgraph(largest_cc)


# In[12]:


expected = nx.closeness_centrality(R, wf_improved=False)


# In[13]:


epsilon=0.2
EW = EWAlgorithm(R, epsilon)
actual = EW.run()

diameter = nx.extrema_bounding(R, compute='diameter')
assert checkAsymptoticConvergence(actual,expected, epsilon, diameter)


# In[14]:


get_ipython().run_line_magic('timeit', '-r 1 EW.run()')



# # Counting triangles

# In[1]:


#import networkx as nx


# In[2]:


#import os
#from path import Path
#PROJ_DIR = Path().getcwd().parent
#DATA_DIR = PROJ_DIR / "data"
#os.chdir (PROJ_DIR)


# In[3]:


#import scripts.src.CountingTriangles as ct


# In[4]:


# import networks
P=nx.read_adjlist(DATA_DIR/"P.adjlist", delimiter=",")
R=nx.read_adjlist(DATA_DIR/"R.adjlist", delimiter=",")


# ## P network

# In[5]:


expected=nx.triangles(P)


# In[6]:


actual=ObviousAlgorithm().run(P)
assert expected==actual


# In[7]:


actual=EnumeratingNeighborPairs().run(P)
assert expected==actual


# In[8]:


actual=DelegatingLowDegreeVertices().run(P)
expected=sum(expected.values())/3
assert expected==actual


# ## R network

# In[9]:


expected=nx.triangles(R)


# In[10]:


actual=EnumeratingNeighborPairs().run(R)
assert expected==actual


# In[11]:


actual=DelegatingLowDegreeVertices().run(R)
expected=sum(expected.values())/3
assert expected==actual

