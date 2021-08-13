"""Test saragraph module."""

from unittest import TestCase
from unittest.mock import patch
from sara.core.sara_graph import SaraGraph, SaraDigraph


class TestSaragraph(TestCase):
    """Test saragraph module."""

    def setUp(self):
        """Executed before each test."""
        self.network = "graph.gml"

    @patch('sara.core.sara_graph.load_graph')
    @patch('sara.core.sara_graph.Centrality')
    def test_saragraph(self, *args):
        """Test saragraph."""
        (mock_centrality, mock_load_graph) = args
        SaraGraph(self.network, False)
        mock_centrality.assert_called()
        mock_load_graph.assert_called()

    @patch('sara.core.sara_graph.load_graph')
    @patch('sara.core.sara_graph.Centrality')
    def test_saradigraph(self, *args):
        """Test saragraph."""
        (mock_centrality, mock_load_graph) = args
        SaraDigraph(self.network, True)
        mock_centrality.assert_called()
        mock_load_graph.assert_called()
