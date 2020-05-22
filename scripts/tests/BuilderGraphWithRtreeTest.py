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


if __name__ == '__main__':
    unittest.main()
