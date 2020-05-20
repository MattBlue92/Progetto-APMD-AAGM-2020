import unittest

import networkx as nx

from scripts.src.BuilderGraph import BuilderGraph
from scripts.src.Tools import Tools
from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger


class BuilderGraphTest(unittest.TestCase, BuilderGraphTestingManeger):
    
    def setUp(self) -> None:
        self.builderGraph = BuilderGraph(0.8)
        self.tools = Tools()

    def testBuildGraphWhenInputsAreCorrectShouldBackAGraph(self):
        df = self.create_dataset_test()
        result = self.builderGraph.buildGraph(df)

        expectedGraph = self.expected_graph_creation(df)
        self.assertTrue(nx.is_isomorphic(expectedGraph, result))


if __name__ == '__main__':
    unittest.main()
