import unittest
import networkx as nx

import scripts.src.CountingTriangles as ct
from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger


class CountingTrianglesTest(unittest.TestCase):

    def setUp(self) -> None:
        manager = BuilderGraphTestingManeger()
        df = manager.create_dataset_test()
        self.graph = manager.expected_graph_creation(df)

    def testObviousAlgorithm(self):
        self.manageCountingTrianglesTesting(ct.ObviousAlgorithm())

    def testEnumeratingNeighborPairs(self):
        self.manageCountingTrianglesTesting(ct.EnumeratingNeighborPairs())

    def testDelegatingLowDegreeVertices(self):
        expectedTriangles = sum(nx.triangles(self.graph).values())/3
        actualTriangles = ct.DelegatingLowDegreeVertices().run(self.graph)
        self.assertEqual(expectedTriangles, actualTriangles)

    def manageCountingTrianglesTesting(self, counter):
        expectedTriangles = nx.triangles(self.graph)
        actualTriangles = counter.run(self.graph)
        self.assertEqual(expectedTriangles, actualTriangles)

if __name__ == '__main__':
    unittest.main()
