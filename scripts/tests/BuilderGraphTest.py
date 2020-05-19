import unittest

import networkx as nx
import numpy as np
import pandas as pd

from scripts.src.BuilderGraph import BuilderGraph
from scripts.src.Tools import Tools


class BuilderGraphTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.builderGraph = BuilderGraph(0.8)
        self.tools = Tools()

    def testBuildGraphWhenInputsAreNoneShouldRiseExp(self):
        df = None
        with self.assertRaises(TypeError):
            self.builderGraph.buildGraph(df)

    def testBuildGraphWhenInputsAreCorrectShouldBackAGraph(self):
        df = {'citta': ['Chieti', 'Acquila', 'Pescara', 'Teramo'],
              'lat': [42.351031167, 42.35122126, 42.46458398, 40.66751177],
              'long': [14.167754574, 13.39843823, 14.2136422, 13.704439971]
              }
        matrixAdj = []
        df = pd.DataFrame(df)
        result = self.builderGraph.buildGraph(df)
        cities = [tuple(city) for city in df[['long', 'lat']].to_numpy()]

        for cityA in cities:
            for cityB in cities:
                matrixAdj.append(self.tools.isConnected(cityA, cityB, 0.8))

        matrixAdj = np.array(matrixAdj)
        matrixAdj = matrixAdj.reshape(df.shape[0], df.shape[0])
        expectedGraph = nx.from_numpy_array(matrixAdj)
        self.assertTrue(nx.is_isomorphic(expectedGraph, result))



if __name__ == '__main__':
    unittest.main()
