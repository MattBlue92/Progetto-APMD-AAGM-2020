import networkx as nx
import numpy as np
import pandas as pd


class BuilderGraphTestingManeger:

    def expected_graph_creation(self, df):
        matrixAdj = []
        cities = [tuple(city) for city in df[['long', 'lat']].to_numpy()]
        for cityA in cities:
            for cityB in cities:
                matrixAdj.append(self.tools.isConnected(cityA, cityB))
        matrixAdj = np.array(matrixAdj)
        matrixAdj = matrixAdj.reshape(df.shape[0], df.shape[0])
        expectedGraph = nx.from_numpy_array(matrixAdj)
        return expectedGraph

    def create_dataset_test(self):
        df = {'citta': ['Chieti', 'Acquila', 'Pescara', 'Teramo'],
              'lat': [42.351031167, 42.35122126, 42.46458398, 42.658918],
              'long': [14.167754574, 13.39843823, 14.2136422, 13.704439971]
              }
        df = pd.DataFrame(df)
        return df

    def testBuildGraphWhenInputsAreNoneShouldRiseExp(self):
        pass

    def testBuildGraphWhenInputsAreCorrectShouldBackAGraph(self):
        pass