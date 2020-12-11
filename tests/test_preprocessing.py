"""Test preProcessing class."""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from sara.core.pre_processing import PreProcessing


class TestPreProcessing(TestCase):
    """TestPreProcessing Class."""

    def setUp(self):
        """Execute before each tests."""
        self.main = PreProcessing()

    @patch('sara.core.pre_processing.isinstance')
    @patch('sara.core.pre_processing._remove_links')
    @patch('sara.core.pre_processing._remove_accents')
    @patch('sara.core.pre_processing._remove_user_mention')
    def test_clean_text_unit(self, *args):
        """unit test clean text."""
        (mock_user_mention, mock_remove_accents, mock_remove_links,
         mock_instance) = args
        text = MagicMock()
        mock_instance.return_value = True
        text.return_value = "A imagem esta disponivel"
        mock_remove_accents.return_value = 'texto limpo'
        mock_user_mention.return_value = 'texto limpo'
        mock_remove_links.return_value = 'texto limpo'
        self.main.clean_text(text)
        mock_instance.assert_called()
        mock_user_mention.assert_called()
        mock_remove_accents.assert_called()
        mock_remove_links.assert_called()

    # integration tests
    def test_clean_text(self):
        """Clean text."""
        expected = "teste base"
        response = self.main.clean_text("Teste @user kkkk sem base")
        self.assertEqual(response, expected)

    def test_clean_text_fail(self):
        """Test Clean text fail case."""
        with self.assertRaises(TypeError):
            self.main.clean_text(["Teste @user kkkk sem base"])

    def test_get_stopwords(self):
        """Test get_stopWords."""
        response = self.main.get_stowords()
        self.assertGreater(len(response), 0)

    def test_remove_links(self):
        """Test remove_links"""
        raw_text = 'A imagem esta disponivel em https://google.com'
        expected = 'imagem disponivel'
        response = self.main.clean_text(raw_text)
        self.assertEqual(response, expected)
