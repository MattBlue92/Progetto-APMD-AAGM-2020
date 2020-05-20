import unittest

import networkx as nx

from scripts.src.Tools import Connections
from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger
from scripts.src.BuilderGraphWithMerge import BuilderGraphWithMerge

class BuilderGraphWithMergeTest(unittest.TestCase,  BuilderGraphTestingManeger):
    def setUp(self) -> None:
        self.builderGraph = BuilderGraphWithMerge(0.8)
        self.tools = Connections(0.8)

    def testBuildGraphWhenInputsAreCorrectShouldBackAGraph(self):
        df = self.create_dataset_test()
        result = self.builderGraph.buildGraph(df)

        expectedGraph = self.expected_graph_creation(df)
        self.assertTrue(nx.is_isomorphic(expectedGraph, result))


if __name__ == '__main__':
    unittest.main()
