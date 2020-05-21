import unittest

import networkx as nx

from scripts.src.Tools import Connections
from scripts.tests.BuilderGraphTestingManeger import BuilderGraphTestingManeger
from scripts.src.BuilderGraphNearestNeighbors import BuilderGraphNearestNeighbors


class BuilderGraphNearestNeighborsTest(unittest.TestCase, BuilderGraphTestingManeger):
    def setUp(self) -> None:
        self.builderGraph = BuilderGraphNearestNeighbors(0.8)
        self.tools = Connections(0.8)

    def testBuildGraphWhenInputsAreCorrectShouldBackAGraph(self):
        df = self.create_dataset_test()
        result = self.builderGraph.buildGraph(df)
        print(result.edges())

        expectedGraph = self.expected_graph_creation(df)
        print(expectedGraph.edges())

        self.assertTrue(nx.is_isomorphic(expectedGraph, result))

    def test_city_subgraph(self):
        df = self.create_dataset_test()
        e=df[df.citta=="Chieti"].values[0]
        result=nx.Graph()
        result.add_edges_from(self.builderGraph.city_subgraph(e,df))

        expectedGraph=nx.Graph()
        expectedGraph.add_edges_from([("Chieti", "Chieti"), ("Chieti", "Acquila"), ("Chieti", "Teramo"), ("Chieti", "Pescara")])

        self.assertTrue(nx.is_isomorphic(expectedGraph, result))



if __name__ == '__main__':
    unittest.main()
