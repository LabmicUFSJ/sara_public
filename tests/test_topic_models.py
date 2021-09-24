from unittest import TestCase
from unittest.mock import MagicMock, patch

from sara.core.topic_model import (lda_scikit, nmf_scikit, generate_tf,
                                   generate_tf_idf)


class TestMain(TestCase):
    """Test main methods."""

    def setUp(self):
        """Execute before each test."""

    @patch('sara.core.topic_model.CountVectorizer')
    def test_generate_tf(self, mock_count_vectorizer):
        """Test generate tf method."""
        mock_corpus = MagicMock()
        mock_count_vectorizer.return_value = MagicMock()
        generate_tf(mock_corpus, 1, False)
        mock_count_vectorizer.assert_called()

    @patch('sara.core.topic_model.TfidfVectorizer')
    def test_generate_tf_idf(self, mock_vectorizer):
        """Test generate tf method."""
        mock_corpus = MagicMock()
        mock_vectorizer.return_value = MagicMock()
        generate_tf_idf(mock_corpus, 1, False)
        mock_vectorizer.assert_called()

    @patch('sara.core.topic_model.LatentDirichletAllocation')
    @patch('sara.core.topic_model.generate_tf')
    def test_lda_scikit(self, *args):
        """Test lda scikit method."""
        (mock_tf, _) = args
        mock_text = MagicMock()
        mock_tf_vectorizer = MagicMock()
        mock_term_frequency = MagicMock()
        mock_tf.return_value = (mock_tf_vectorizer, mock_term_frequency)
        lda_scikit(mock_text, 1, False)
        mock_tf.assert_called()

    @patch('sara.core.topic_model.NMF')
    @patch('sara.core.topic_model.generate_tf_idf')
    def test_nmf_scikit(self, *args):
        """Test nmf scikit method."""
        (mock_tf, _) = args
        mock_text = MagicMock()
        mock_tf_vectorizer = MagicMock()
        mock_term_frequency = MagicMock()
        mock_tf.return_value = (mock_tf_vectorizer, mock_term_frequency)
        nmf_scikit(mock_text, 1, False)
        mock_tf.assert_called()
