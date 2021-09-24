"""Botometer tests."""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from sara.core.botometer_api import (check_users_botometer,
                                     check_user_botometer)


class TestBotometer(TestCase):
    """Test Botometer methods."""

    @patch('sara.core.botometer_api.TWITTER_KEYS')
    @patch('sara.core.botometer_api.rapidapi_key')
    def setUp(self, *args):
        """Execute before each tests."""
        (_, _) = args

    @patch('botometer.Botometer.check_accounts_in')
    def test_check_users_botometer(self, botometer_mock):
        """Test method to get accounts Botometer score."""
        expected = {"1": "score", "2": "score"}
        botometer_mock.return_value = expected
        response = check_users_botometer(['1', '2'])
        botometer_mock.assert_called()
        self.assertEqual(response, expected)

    @patch('botometer.Botometer.check_account')
    def test_check_user_botometer(self, mock_botometer):
        botometer_score = {'1': 'score'}
        mock_botometer.return_value = botometer_score
        response = check_user_botometer(['1'])
        mock_botometer.assert_called()
        self.assertEqual(response, botometer_score)
