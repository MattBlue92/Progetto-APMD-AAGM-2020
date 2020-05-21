import networkx as nx


from scripts.src.BuilderGraph import BuilderGraph


class BuilderGraphNearestNeighbors(BuilderGraph):
    def __init__(self, d):
        super().__init__(d)

    def buildGraph(self, df):
        if df is None:
            raise TypeError("Inputs are not not valide. long or lat is None. Please insert valid data!")

        list_edges=[]
        df.apply(lambda e: list_edges.extend(self.city_subgraph(e,df.copy())), axis=1)
        graph=nx.Graph()
        graph.add_edges_from(list_edges)
        return graph

    def city_subgraph(self, e, df):
        df["long"] = abs(df["long"] - e[2])
        df["lat"] = abs(df["lat"] - e[1])
        long_sort = df.sort_values(by=['long'], kind='mergesort')
        lat_sort = df.sort_values(by=['lat'], kind='mergesort')

        long_sort=long_sort.values
        lat_sort=lat_sort.values

        long_cities = self.create_adjacent_cities(long_sort)
        lat_cities=self.create_adjacent_cities(lat_sort)

        list_edges=[]
        for x in long_cities:
            if x in lat_cities:
                list_edges.append((e[0], x))
        return list_edges

    def create_adjacent_cities(self, sorted_list):
        adjacent_cities = []
        i = 0
        end_list = False
        while (not end_list and i < sorted_list.shape[0]):
            if sorted_list[i][2] <= self.d:
                adjacent_cities.append(sorted_list[i][0])
            else:
                end_list=True
            i = i + 1
        return adjacent_cities