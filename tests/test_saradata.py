from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from sara.core.sara_data import SaraData


class TestSaraData(TestCase):
    """Test SaraData class."""

    @patch('sara.core.sara_data.get_client')
    def setUp(self, mock_get_client):
        """Startup method."""
        self.main = SaraData()
        mock_get_client.assert_called()

    @patch('sara.core.sara_data.load_tweets')
    def test_get_tweets(self, mock_load_tweets):
        """Test get tweets method."""
        self.main.get_tweets()
        mock_load_tweets.assert_called()

    @patch('sara.core.sara_data.load_database')
    def test_get_projected_data_fail_case(self, mock_load_database):
        """Test get projected_data."""
        with self.assertRaises(TypeError):
            self.main.get_projected_data()

    @patch('sara.core.sara_data.load_database')
    def test_get_projected_data(self, mock_load_database):
        """Test get projected_data."""
        self.main.get_projected_data({"text": 1}, 0)
        mock_load_database.assert_called()
