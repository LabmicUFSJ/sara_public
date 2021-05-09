# -*- coding: utf-8 -*-
"""Get network centrality."""
import networkx as nx

from sara.core.config import centrality_path
from sara.core.utils import create_path

create_path(centrality_path)


class Centrality:
    """Centrality Class."""

    def __init__(self, network):
        """Centrality Class.
           ARGS: nx.Graph or nx.DiGraph.
        """
        # This check is not pythonic.
        # An pattern project to return type is best
        if isinstance(network, nx.DiGraph):
            self.directed = True
        elif isinstance(network, nx.Graph):
            self.directed = False
        else:
            raise TypeError('Invalid network type.')
        self.network = network
        self.betweenness_list = self.get_betweenness()
        self.degree_list = self.get_degree()
        if self.directed:
            self.pagerank_list = self.get_pagerank()

    @property
    def stats(self):
        """Return Graph Stats."""
        return nx.info(self.network)

    @staticmethod
    def __get_dict(elements_list):
        """Return a dict."""
        return {element[0]: element[1] for element in elements_list}

    @staticmethod
    def __get_key(item):
        """Return item."""
        return item[1]

    def get_betweenness(self):
        """Get list with betweenness centrality."""
        betweenness = nx.betweenness_centrality(self.network)
        return self.__get_ordered_list(betweenness)

    def get_pagerank(self):
        """Get list with pagerank centrality."""
        if not self.directed:
            raise ValueError('Pagerank is not available in undirected network')
        rank = nx.pagerank(self.network)
        return self.__get_ordered_list(rank)

    def get_degree(self):
        """Get list with degree centrality."""
        degree = nx.degree_centrality(self.network)
        return self.__get_ordered_list(degree)

    def __get_ordered_list(self, elements):
        """Get ordered_list."""
        list_ordered = [[i, elements[i]] for i in elements]
        return sorted(list_ordered, key=self.__get_key, reverse=True)

    def write_seeds(self):
        """Write file with nodes ordered by centrality importance."""
        seeds = self.as_dict()
        print(f"Writing seeds in {centrality_path}")
        for key, items in seeds.items():
            path_to_save = f'{centrality_path}_{key}_seeds.txt'
            with open(path_to_save, 'w') as arq_seeds:
                for seed in items:
                    arq_seeds.write(str(seed) + "\n")

    def get_high_centrality_nodes(self):
        """Get nodes with high centrality.
        Graph (Undiretected)
            Return {'betweenness': list,'degree': list}.
        Digraph (Directed)
            Return {'betweenness': list,'degree': list,'pagerank': list}.
        """
        if self.directed:
            return {"betweenness": self.betweenness_list[0],
                    "degree": self.degree_list[0],
                    "pagerank": self.pagerank_list[0]}
        return {"betweenness": self.betweenness_list[0],
                "degree": self.degree_list[0]}

    def as_dict(self):
        """Return a dict."""
        if self.directed:
            return {'betweenness': self.__get_dict(self.betweenness_list),
                    'degree': self.__get_dict(self.degree_list),
                    'pagerank': self.__get_dict(self.pagerank_list)}
        return {'betweenness': self.__get_dict(self.betweenness_list),
                'degree': self.__get_dict(self.degree_list)}
