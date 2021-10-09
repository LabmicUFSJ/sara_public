"""Tests to networks module."""
from unittest import TestCase
from unittest.mock import MagicMock, patch
from sara.core.network_generators import (
    get_mentions_network,
    get_weighted_mentions_network,
    get_weigthed_retweet_network,
    get_retweets_network,
)


class TestNetworks(TestCase):
    """Test Networks generators."""

    def setUp(self):
        """This method run before the each tests."""
        self.mention_tweets = [
            {
                "user": {"screen_name": "user1"},
                "entities": {
                    "user_mentions": [
                        {"screen_name": "user2"},
                        {"screen_name": "user3"},
                    ]
                },
            }
        ]
        self.retweet_tweets = [
            {
                "user": {"screen_name": "user1"},
                "retweeted_status": {
                    "user": {"screen_name": "user2"},
                },
            }
        ]

    def test_mentions_network(self):
        """Test mentions network."""
        graph = get_mentions_network(self.mention_tweets, True)
        self.assertEqual(len(graph.nodes), 3)

    def test_weighted_mentions_network(self):
        """Test weighted mentions network."""
        graph = get_weighted_mentions_network(self.mention_tweets, True)
        self.assertEqual(len(graph.nodes), 3)

    @patch('sara.core.network_generators.mentions_network.validate_input')
    @patch('sara.core.network_generators.mentions_network.get_networkx_instance')
    def test_mentions_network_with_mock(self, *args):
        """Test method to generate mention network using mock."""
        (mock_get_network, mock_validate_input) = args
        mock_graph = MagicMock()
        mock_get_network.return_value = mock_graph
        get_mentions_network(self.mention_tweets, True)
        mock_validate_input.assert_called()
        mock_get_network.assert_called()
        self.assertEqual(mock_graph.add_edge.call_count, 2)

    def test_retweet_network(self):
        """Test retweet network."""

        graph = get_retweets_network(self.retweet_tweets, True)
        self.assertEqual(len(graph.nodes), 2)

    def test_weighted_retweet_network(self):
        """Test weighted retweet network."""

        graph = get_weigthed_retweet_network(self.retweet_tweets, True)
        self.assertEqual(len(graph.nodes), 2)
