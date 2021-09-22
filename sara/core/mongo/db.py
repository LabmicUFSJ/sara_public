# -*- coding: utf-8 -*-
"""DB"""
import random
import sys

import pymongo
from pymongo.errors import ConnectionFailure

from sara.core.pre_processing import PreProcessing

pre_processing = PreProcessing()


# pylint: disable=R0903, C0103
class SingletonClient:
    """Generate a singleton the MongoDB client."""
    class __SingletonClient:
        def __init__(self):
            # Initialise mongo client
            self.client = pymongo.MongoClient('localhost', 27017)

    __instance = None

    def __init__(self):
        if not SingletonClient.__instance:
            SingletonClient.__instance = SingletonClient.__SingletonClient()

    def __getattr__(self, item):
        return getattr(self.__instance, item)


def get_client():
    """Return an instance of the MongoDB client."""
    client = SingletonClient().client
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure:
        print("Server not available, please run mongodb")
        print("You can run mongodb using: sudo service mongod start")
        sys.exit(-1)
    return client


def load_database(client, database_name, collection):
    """Load database."""
    database = client[database_name]
    return database[collection]


def load_users(database_name, collection, number_users):
    """
    Returns a list with no duplicate users.
    """
    client = get_client()
    collection = load_database(client, database_name, collection)
    total_documents = collection.count_documents({})
    consult_number = total_documents if number_users is None else number_users
    projection = {"user": 1, "retweeted_status.user": 1}
    users = collection.find({}, projection).limit(consult_number*2)
    users_dict = {}
    for user in users:
        retweeted = user.get('retweeted_status')
        if retweeted:
            usr_retweeted_id = retweeted['user']['id']
            users_dict[usr_retweeted_id] = retweeted['user']
        if not user.get('user'):
            continue
        user_id = user['user']['id']
        users_dict[user_id] = user['user']
    print(f"Number of recovered users: {len(users_dict)}")
    unique_users = len(users_dict) if number_users is None else number_users
    return random.sample(list(users_dict.values()), k=unique_users)


def return_users(database_name, collection, users_id):
    """Returns the list of users."""
    client = get_client()
    cursor = load_database(client, database_name, collection)
    users = [cursor.find({"user.id_str": usr_id}
                         )[0]['user'] for usr_id in users_id]
    return users


# pylint:disable=R1721
def load_tweets(database_name, collection_name, tweet_limit=None):
    """
    Return a list of tweets.
    """
    client = get_client()
    collection = load_database(client, database_name, collection_name)
    if tweet_limit:
        tweets = collection.find().limit(tweet_limit)
    tweets = collection.find()
    return [tweet for tweet in tweets]


def get_clean_tweets_txt(database_name, collection_name):
    """Load tweets and apply `pre_processing` to clean tweets.

    Return a list of clean tweets.
    """
    client = get_client()
    collection = load_database(client, database_name, collection_name)
    tweets = collection.find()
    tweet_list = []
    for tweet in tweets:
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
        except KeyError:
            full_tweet = tweet['text']
        if len(full_tweet) < 1:
            continue
        tweet_list.append(pre_processing.clean_text(full_tweet))
    return tweet_list


def get_tweets_txt(database_name, collection_name):
    """Return raw text from tweets."""
    client = get_client()
    collection = load_database(client, database_name, collection_name)
    tweets = collection.find()
    tweet_list = []
    for tweet in tweets:
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
        except KeyError:
            full_tweet = tweet['text']
        if len(full_tweet) < 1:
            continue
        tweet_list.append(full_tweet)
    return tweet_list
