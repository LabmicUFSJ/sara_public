"""Test Database class."""
from unittest import TestCase
from unittest.mock import patch

from sara.core.mongo.db import SingletonClient, get_client, load_users


class TestDatabase(TestCase):
    """TestDatabase class."""

    @patch('sara.core.mongo.db.pymongo')
    def setUp(self, *args):
        """Execute before each test."""
        _ = args[0]
        self.client = SingletonClient()

    def test_singleton(self):
        """Test MongoDB singleton class."""
        instance = self.client.client
        instanace2 = self.client.client
        self.assertEqual(id(instance), id(instanace2))

    def test_get_client(self):
        """Test get_client."""
        instance1 = get_client()
        instance2 = get_client()
        self.assertEqual(id(instance1), id(instance2))

    def test_load_users(self):
        """Test load users."""
        load_users("test", "collection_test", 0)
        client = self.client.client.__getitem__().__getitem__()
        self.assertEqual(client.find().limit.call_count, 1)
