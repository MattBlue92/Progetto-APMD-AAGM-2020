import unittest
import networkx as nx

from scripts.src.BuiderGraphWithRtree import BuilderGraphWithRtree
from scripts.src.Tools import Connections
from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger


class BuilderGraphWithRteeTest(unittest.TestCase,  BuilderGraphTestingManeger):
    def setUp(self) -> None:
        self.df = self.create_dataset_test()
        self.builderGraph = BuilderGraphWithRtree(0.8, self.df)
        self.tools = Connections(0.8)

    def testBuildGraphWhenInputsAreCorrectShouldBackAGraph(self):
        result = self.builderGraph.intersection()
        expectedGraph = self.expected_graph_creation(self.df)
        self.assertTrue(nx.is_isomorphic(expectedGraph, result))

    def testBuildGraphWithWeight(self):
        result=self.builderGraph.intersection(flag=True)
        expectedGraph=self.weighted_graph_creation(self.df)
        self.assertEqual(expectedGraph.adj.items(), result.adj.items())

    def weighted_graph_creation(self, df):
        graph = self.expected_graph_creation(df)
        mapping={0:'Chieti', 1:'Acquila', 2:'Pescara', 3:'Teramo'}
        nx.relabel_nodes(graph, mapping,  copy=False)
        for n, nbrs in graph.adj.items():
            for nbr in nbrs.keys():
                graph[n][nbr]['weight']=self.euclidean_distance(n, nbr, df)
        return graph

    def euclidean_distance(self, n, nbr, df):
        from math import sqrt
        x_1=df[df["citta"]==n].long.values[0]
        x_2=df[df["citta"] == n].lat.values[0]
        y_1=df[df["citta"]==nbr].long.values[0]
        y_2=df[df["citta"] == nbr].lat.values[0]
        return sqrt((x_1-x_2)**2+(y_1-y_2)**2)



if __name__ == '__main__':
    unittest.main()
