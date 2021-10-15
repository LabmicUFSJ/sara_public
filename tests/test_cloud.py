"Test tag cloud"
from unittest import TestCase
from unittest.mock import patch
from sara.core.cloud import cloud_lda


class TestCloud(TestCase):
    """Test module related to TFIDF"""

    def setUp(self):
        pass

    @patch('sara.core.cloud.make_cloud')
    def test_cloud_lda(self, mock_make_cloud):
        """Test make cloud."""
        lista_tweets = [[5, " tweet texto 1"], [5, "tweet texto 2"]]
        n_repeticoes = 10
        cloud_lda(lista_tweets, n_repeticoes)
        mock_make_cloud.assert_called()
