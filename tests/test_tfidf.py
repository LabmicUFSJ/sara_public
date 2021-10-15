"test tfidf"
from unittest import TestCase
from unittest.mock import MagicMock, patch
from sara.core.tf_idf import get_tf_idf


class TestTF(TestCase):
    """Test module related to TFIDF"""

    def setUp(self):
        pass

    @patch('sara.core.tf_idf.TfidfVectorizer')
    def test_test_get_tfidf(self, mock_vectorizer):
        """Test generate TFIDF method."""
        mock_corpus = MagicMock()
        mock_vectorizer.return_value = MagicMock()
        get_tf_idf(mock_corpus)
        mock_vectorizer.assert_called()
