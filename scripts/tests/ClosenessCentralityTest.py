import unittest

from scripts.src.ClosenessCentrality import ClosenessCentralityBFS, EWAlgorithm

from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger
import networkx as nx
import  numpy as np

class ClosenessCentralityTest(unittest.TestCase):

    def setUp(self) -> None:
        manager = BuilderGraphTestingManeger()
        df = manager.create_dataset_test()
        self.graph = manager.expected_graph_creation(df)
        self.disconnectedGraph=manager.createDisconnectedGraph()

    def testClosenessCentralityUsingBFS(self):
        CCBFS = ClosenessCentralityBFS()
        actualy = CCBFS.run(self.graph)
        expected = nx.closeness_centrality(self.graph, wf_improved=False)
        self.assertEqual(expected, actualy)

    def testClosenessUsingEWAlgorithm(self):
        epsilon = 0.06
        n = 1000
        m = 2000
        G = nx.gnm_random_graph(n, m, seed=42)

        largest_cc = max(nx.connected_components(G), key=len)
        G=G.subgraph(largest_cc)
        EW = EWAlgorithm(G, epsilon)
        actualy = EW.run()
        expected = nx.closeness_centrality(G, wf_improved=False)
        d = nx.diameter(G)
        self.assertTrue(self.checkAsymptoticConvergence(expected, actualy, epsilon,d))

    def checkAsymptoticConvergence(self, expected, actual, epsilon, d):
        result = True
        for key in actual.keys():
            c_hat = 1 / actual[key]
            c = 1 / expected[key]
            abs_error = abs(c_hat - c)
            if abs_error>=epsilon*d:
                print("actual: {}, expected: {}, error: {}".format(c_hat, c, abs_error))
            result = result and abs_error < epsilon*d
        return result

    def testDistance_dict_bfs(self):
        G = nx.house_graph()
        EW = EWAlgorithm(G,0.43)
        actual = EW.distance_dict_bfs(G,4)
        expected = {4:0, 3: 1, 2:1, 1:2, 0:2 }
        self.assertEqual(actual,expected)

if __name__ == '__main__':
    unittest.main()
