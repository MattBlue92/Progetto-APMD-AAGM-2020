import unittest

from scripts.src.ClosenessCentrality import ClosenessCentrality
from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger
import networkx as nx
import  numpy as np

class ClosenessCentralityTest(unittest.TestCase):

    def setUp(self) -> None:
        manager = BuilderGraphTestingManeger()
        df = manager.create_dataset_test()
        self.graph = manager.expected_graph_creation(df)
        self.closeness = ClosenessCentrality()
        self.disconnectedGraph=manager.createDisconnectedGraph()

    def testClosenessCentralityUsingBFS(self):
        actualy = self.closeness.closenessUsingBFS(self.graph)
        expected = nx.closeness_centrality(self.graph, wf_improved=False)
        self.assertEqual(expected, actualy)

    def testClosenessCentralityUsingBFSwithIsolatedNode(self):
        G = nx.Graph()
        G.add_node(1)
        actualy = self.closeness.closenessUsingBFS(G)
        expected = nx.closeness_centrality(G, wf_improved=False)
        self.assertEqual(expected, actualy)

    def testClosenessCentralityUsingBFSWithDisconnectedGraph(self):
        actualy=self.closeness.closenessUsingBFS(self.disconnectedGraph, networkx=True)
        expected=nx.closeness_centrality(self.disconnectedGraph, wf_improved=False)
        self.assertEqual(expected, actualy)


    def testClosenessUsingEWAlgorithm(self):
        epsilon = 0.5
        n = 100
        m = 200
        G = nx.gnm_random_graph(n, m, seed=42)

        largest_cc = max(nx.connected_components(G), key=len)
        G=G.subgraph(largest_cc)
        actualy = self.closeness.closenessUsingEWAlgorithm(G, epsilon)
        expected = nx.closeness_centrality(G, wf_improved=False)
        self.assertTrue(self.checkAsymptoticConvergence(expected, actualy, epsilon))

    def checkAsymptoticConvergence(self, expected, actual, epsilon):
        result = True
        for key in actual.keys():
            c_hat = 1 / actual[key]
            c = 1 / expected[key]
            abs_error = abs(c_hat - c)
            print("actual: {}, expected: {}, error: {}".format(c_hat, c, abs_error))
            result = result and abs_error < epsilon
        return result

if __name__ == '__main__':
    unittest.main()
