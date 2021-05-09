"""centrality tests."""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from sara.core.centrality import Centrality
import networkx as nx


def begin_lists(instance):
    """Initiatilize lists."""
    instance.betweenness_list = [['node_betweenness', 1]]
    instance.degree_list = [['node_degree', 1]]
    instance.pagerank_list = [['node_pagerank', 1]]
    return instance


class TestCentrality(TestCase):
    """TestCentrality Class."""

    @patch('sara.core.centrality.Centrality.get_betweenness')
    @patch('sara.core.centrality.Centrality.get_degree')
    @patch('sara.core.centrality.Centrality.get_pagerank')
    def setUp(self, *_):
        """Execute before each tests."""
        self.digraph= MagicMock(spec=nx.DiGraph)
        self.main_digraph = Centrality(self.digraph)
        self.main_digraph = begin_lists(self.main_digraph)

        self.graph = MagicMock(spec=nx.Graph)
        self.main_graph = Centrality(self.graph)
        self.main_graph = begin_lists(self.main_graph)

    @patch('networkx.betweenness_centrality')
    def test_get_betweenness(self, mock_networkx):
        """Test betweenness."""
        self.main_digraph.get_betweenness()
        mock_networkx.assert_called()

    @patch('networkx.degree_centrality')
    def test_get_degree(self, mock_networkx):
        """Test get_degree."""
        self.main_digraph.get_degree()
        mock_networkx.assert_called()

    @patch('networkx.pagerank')
    def test_get_pagerank(self, mock_networkx):
        """Test get pagerank."""
        self.main_digraph.get_pagerank()
        mock_networkx.assert_called()

    def test_get_high_centrality_nodes(self):
        """Test get_high_centrality_nodes."""

        expected = {'betweenness': ['node_betweenness', 1],
                    'degree': ['node_degree', 1],
                    'pagerank': ['node_pagerank', 1]}

        response = self.main_digraph.get_high_centrality_nodes()
        self.assertEqual(response, expected)

    def test_fail_get_high_centrality_nodes(self):
        """Test fail case get_high_centrality_nodes."""
        self.main_digraph.betweenness_list = []
        with self.assertRaises(IndexError):
            self.main_digraph.get_high_centrality_nodes()

    def test_as_dict(self):
        """Test as_dict to directed network."""
        expected = {'betweenness': {'node_betweenness': 1},
                    'degree': {'node_degree': 1},
                    'pagerank': {'node_pagerank': 1}}
        response = self.main_digraph.as_dict()
        self.assertEqual(expected, response)

        # test fail case
        response = self.main_graph.as_dict()
        self.assertNotEqual(response, expected)

    def test_graph_as_dict(self):
        """Test as_dict to undirected network."""
        expected = {'betweenness': {'node_betweenness': 1},
                    'degree': {'node_degree': 1}}
        response = self.main_graph.as_dict()
        self.assertEqual(expected, response)

    @patch('networkx.info')
    def test_get_stats(self, mock_networkx):
        """Test get stats."""
        self.main_graph.stats()
        mock_networkx.assert_called()
