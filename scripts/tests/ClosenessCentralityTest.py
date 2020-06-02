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

    def testClosenessCentralityUsingUtilities(self):
        actualy = self.closeness.closenessUsingUtilities(self.graph)
        expected = nx.closeness_centrality(self.graph, wf_improved=False)
        self.assertEqual(expected, actualy)

    def testClosenessCentralityUsingUtilitiesWithDisconnectedGraph(self):
        actualy=self.closeness.closenessUsingUtilities(self.disconnectedGraph, networkx=True)
        expected=nx.closeness_centrality(self.disconnectedGraph, wf_improved=False)
        self.assertEqual(expected, actualy)

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

    def testClosenessCentralityUsingUtilitieswithIsolatedNode(self):
        G = nx.Graph()
        G.add_node(1)
        actualy = self.closeness.closenessUsingUtilities(G)
        expected = nx.closeness_centrality(G, wf_improved=False)
        self.assertEqual(expected, actualy)

    def testClosenessUsingEWAlgorithm(self):
        epsilon = 0.5
        n = 100
        m = 200
        G = nx.gnm_random_graph(n, m, seed=42)
        actualy = self.closeness.closenessUsingEWAlgorithm(G, epsilon)
        expected = self.closeness.closenessUsingUtilities(G)
        result = True
        for key in actualy.keys():
            abs_error = np.abs((1 / (actualy[key]+0.5)) - (1 / (expected[key]+0.5)))
            result = result and abs_error < epsilon
        self.assertTrue(result)

    def testArmonicCloseness(self):
        actualy = self.closeness.armonicCloseness(self.graph)
        expected = nx.harmonic_centrality(self.graph)
        self.assertEqual(expected, actualy)

if __name__ == '__main__':
    unittest.main()
