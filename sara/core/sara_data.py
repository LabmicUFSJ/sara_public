"""SaraData"""
import queue
import threading

from sara.core.config import DATABASE as default_database
from sara.core.config import sara_files_path
from sara.core.mongo.db import get_client, load_database, load_tweets
from sara.core.sara_file.db import load_data, save_data_file
from sara.core.utils import create_path

tweets_queue = queue.Queue()


def storage_mongodb():
    """Queue to save data in MongoDB."""
    while True:
        tweet, connection = tweets_queue.get()
        connection.replace_one(tweet, tweet, True)
        tweets_queue.task_done()


# Use thread to save data in database.
threading.Thread(target=storage_mongodb, daemon=True).start()


class SaraData:
    """
    Encapsule the backeend to store and load the data.
    """
    def __init__(self, collection_name=None, database=None,
                 storage_type='mongodb'):
        """SaraData arguments, collection_name and storage_type."""

        if database:
            self.database = database
        else:
            # default database
            self.database = default_database

        self.collection = collection_name
        # backend to store the data.
        self.storage_type = storage_type
        if 'mongodb' in self.storage_type:
            print('using mongodb')
            self.client = get_client()
        elif 'sarafile' in storage_type:
            print('using SaraFile')
            self.sara_file_storage = f'{sara_files_path}/{self.collection}'
            create_path(self.sara_file_storage)

    def update_database(self, database):
        """Update database used."""
        self.database = database
        print(f'Database updated to {self.database}')

    def get_tweets(self, number_tweets=None):
        """Get tweets.
        if number_tweets is not defined, return all the database.

        Return a list with tweets in JSON.
        """
        if 'mongodb' in self.storage_type:
            print("Use get_projected_data to load a big number of data.")
            return load_tweets(self.database, self.collection, number_tweets)
        if 'sqlite' in self.storage_type:
            pass
        if 'sarafile' in self.storage_type:
            return load_data(self.collection)
        return None

    def get_projected_data(self, project, number_tweets):
        """Get filtered data"""
        conn = load_database(self.client, self.database, self.collection)
        return conn.find(projection=project).limit(number_tweets)

    def get_filtered_tweet(self, proj_filter, project, number):
        """Get filtered data."""
        conn = load_database(self.client, self.database, self.collection)
        return conn.find(proj_filter, projection=project).limit(number)

    def count_recovered_documments(self, proj_filter, number):
        """Return number the elements returned by the query the Mongo."""
        conn = load_database(self.client, self.database, self.collection)
        recovered = conn.count_documents(proj_filter, limit=number)
        return recovered

    def save_data(self, data):
        """Save data."""
        if 'mongodb' in self.storage_type:
            conn = load_database(self.client, self.database, self.collection)
            # to store in database
            tweets_queue.put((data, conn))

        if 'sarafile' in self.storage_type:
            save_data_file(f'{self.sara_file_storage}/{self.collection}', data)

    def get_all_collections(self):
        """Return all collections from a database."""
        collections_list = []
        if 'mongodb' in self.storage_type:
            database = self.client[self.database].collection_names()
            for collection_name in database:
                collections_list.append(collection_name)
        return collections_list
