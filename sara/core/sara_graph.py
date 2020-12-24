"""Graph class"""
import networkx as nx

from sara.core.centrality import Centrality


def load_graph(network_path):
    """Load a Graph with '.gml', '.gexf' or .edgelist'."""
    if network_path.endswith('.gml'):
        return nx.read_gml(network_path, "id")
    if network_path.endswith('.gexf'):
        return nx.read_gexf(network_path)
    if network_path.endswith('.edgelist'):
        return nx.read_edgelist('.edgelist')
    raise TypeError(f'This network format {network_path} is not supported,'
                    'supported extensions: .gml, .edgelist, .gexf \n')


class SaraGraph:
    """SaraGraph."""
    def __init__(self, network_path, directed=False):
        if isinstance(network_path, nx.Graph):
            self.network_path = ''
            self.directed = directed
            self.network = network_path
        else:
            self.network_path = network_path
            self.directed = directed
            self.network = load_graph(network_path)
        self.centrality = Centrality(self.network)

    def get_centrality(self):
        """Return centrality."""
        return self.centrality

    def get_network_path(self):
        """Return network path."""
        return self.network_path


class SaraDigraph:
    """SaraDigraph."""
    def __init__(self, network_path, directed=True):
        if isinstance(network_path, nx.DiGraph):
            self.network_path = ''
            self.directed = directed
            self.network = network_path
        else:
            self.network_path = network_path
            self.directed = directed
            self.network = load_graph(network_path)
        self.centrality = Centrality(self.network)

    def get_centrality(self):
        """Return centrality."""
        return self.centrality

    def get_network_path(self):
        """Return network path."""
        return self.network_path
