"""Test utils module."""
from unittest import TestCase
from unittest.mock import MagicMock

from sara.core.utils import get_hashtags


class TestUtils(TestCase):
    """Test utils class."""

    def setUp(self):
        """Run before each test."""

    def test_get_hashtags(self):
        """test get hashtags."""
        tweets = MagicMock()
        expected = [('teste1', 1)]
        data = {'entities': {'hashtags': [{'text': 'teste1'}]}}
        tweets.__getitem__.side_effect = data.__getitem__
        response = get_hashtags([tweets], 1)
        self.assertEqual(response, expected)
