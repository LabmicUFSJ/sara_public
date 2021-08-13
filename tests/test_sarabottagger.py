"""Test saraBottagger"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from sara.core.sarabottagger import SaraBotTagger


class SarabotTaggerTestCase(TestCase):
    """SaraBotTagger module."""

    @patch('sara.core.sarabottagger.valid_model')
    @patch('sara.core.sarabottagger.load')
    @patch('sara.core.sarabottagger.create_path')
    def setUp(self, *args):
        """Execute before each test."""
        (mock_create_path, mock_load, mock_valid_model) = args
        database = "database"
        collection = "collection"
        model = "model"
        self.main = SaraBotTagger(database, collection, 0, model)
        mock_create_path.assert_called()
        mock_load.assert_called()
        mock_valid_model.assert_called()

    @patch('sara.core.sarabottagger.SaraBotTagger.get_proba')
    @patch('sara.core.sarabottagger.SaraBotTagger._is_bot')
    @patch('sara.core.sarabottagger.get_user_from_dict')
    @patch('sara.core.sarabottagger.load_users')
    @patch('sara.core.sarabottagger._save_list')
    def test_sarabottagger(self, *args):
        (mock_save_list, mock_load_users, mock_get_users,
         mock_is_bot, mock_get_proba) = args
        mock_get_users.as_dict = {
                                    'id_str': 548,
                                    'human_prob': 0.80,
                                    'bot_prob': 0.20,
                                    'final_class': 'human'
                                }
        mock_is_bot.return_value = 0
        mock_get_proba.return_value = [[[0.8], [0.2]], [0]]
        mock_load_users.return_value = [MagicMock()]
        response = self.main.run()
        mock_load_users.assert_called()
        mock_save_list.assert_called()
        self.assertEqual(len(response[0]), 1)
