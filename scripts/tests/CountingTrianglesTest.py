import unittest

from scripts.src.CountingTriangles import CountingTriangles
from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger
import networkx as nx


class CountingTrianglesTest(unittest.TestCase):

    def setUp(self) -> None:
        manager = BuilderGraphTestingManeger()
        df = manager.create_dataset_test()
        self.graph = manager.expected_graph_creation(df)
        self.triangles = CountingTriangles()

    def testObviusAlgo(self):
        expectedTriangles = nx.triangles(self.graph)
        actualTriangles = self.triangles.obviusAlgo(self.graph)
        self.assertEqual(expectedTriangles, actualTriangles)

    def testalgoEnum(self):
        expectedTriangles = nx.triangles(self.graph)
        actualTriangles = self.triangles.algoEnum(self.graph)
        print(actualTriangles)
        self.assertEqual(expectedTriangles, actualTriangles)

    def testLowDregree(self):
        expectedTriangles = sum(nx.triangles(self.graph).values())/3
        actualTriangles = self.triangles.lowDregree(self.graph)
        self.assertEqual(expectedTriangles, actualTriangles)




if __name__ == '__main__':
    unittest.main()
