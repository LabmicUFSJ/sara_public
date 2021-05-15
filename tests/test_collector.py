"""
Test SaraCollector
"""
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from sara.core.collector import SaraCollector


class TestSaraCollector(TestCase):
    """Test SaraCollector module."""

    @patch('sara.core.collector.SaraData', new=mock.Mock)
    @patch('sara.core.collector.get_twitter_api')
    def setUp(self, *args):
        """Startup method."""
        (mock_credentials) = args
        mock_credentials = mock_credentials[0]
        self.api_mock = MagicMock()
        mock_credentials.return_value = self.api_mock
        self.storage_mock = MagicMock()
        self.collector = SaraCollector(self.storage_mock)

    def test_real_time_collector(self):
        """Test real time collector."""
        term = "test mock"
        self.api_mock.GetStreamFilter.return_value = [MagicMock(), MagicMock()]
        self.collector.real_time_collector(term)
        self.assertEqual(self.storage_mock.save_data.call_count, 2)

    def test_real_time_collector_with_limit(self):
        """Test real time collector with limit."""
        term = "test mock"
        self.api_mock.GetStreamFilter.return_value = [MagicMock(), MagicMock()]
        self.collector.real_time_collector(term, 2)
        self.assertEqual(self.storage_mock.save_data.call_count, 2)

    def test_scheduled(self):
        """Test scheduled collector."""
        term = "test mock"
        self.api_mock.GetStreamFilter.return_value = [MagicMock(), MagicMock()]
        self.collector.scheduled(term, 2)
        self.assertEqual(self.storage_mock.save_data.call_count, 2)

    def test_collector_followers(self):
        """Test collector followers."""
        user_id = '1234'
        next_mock = MagicMock()
        previous_mock = MagicMock()
        users_recovered = MagicMock()
        followed_data = (next_mock, previous_mock, [users_recovered])
        self.api_mock.GetFollowersPaged.return_value = followed_data
        self.collector.collector_followers(user_id)
        self.assertEqual(self.storage_mock.save_data_file.call_count, 1)
