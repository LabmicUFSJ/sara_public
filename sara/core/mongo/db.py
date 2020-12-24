# -*- coding: utf-8 -*-
"""DB"""
import random
import sys
from pymongo import MongoClient

from sara.core.pre_processing import PreProcessing

pre_processing = PreProcessing()


def get_client():
    """Inicia a conexão com o mongoDb."""
    return MongoClient('localhost', 27017)


def load_database(client, name, collection):
    """Carrega um banco com uma colecao."""
    database = client[name]
    return database[collection]


def load_users(database_name, collection, number_users):
    """
    Carrega e retorna uma lista de usuários.
    Return a list not duplicated the users.
    """
    client = get_client()
    collection = load_database(client, database_name, collection)
    total_documents = collection.count_documents({})
    consult_number = total_documents if number_users is None else number_users
    users = collection.find({}, {"user": 1, "retweeted_status.user":1}).limit(consult_number*2)
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
    print(f"Número de usuários unicos recuperados: {len(users_dict)}")
    unique_users = len(users_dict) if number_users is None else number_users
    client.close()
    return random.sample(list(users_dict.values()), k=unique_users)


def return_users(database_name, collection, users_id):
    """Return users."""
    client = get_client()
    cursor = load_database(client, database_name, collection)
    users = [cursor.find({"user.id_str": usr_id}
                         )[0]['user'] for usr_id in users_id]
    client.close()
    return users


# pylint:disable=R1721
def load_tweets(nome_banco, colecao, limite=None):
    """
    Carrega Tweets.
    Return a tweet list.
    """
    cliente = get_client()
    colecao = load_database(cliente, nome_banco, colecao)
    if limite:
        tweets = colecao.find().limit(limite)
    tweets = colecao.find()
    cliente.close()
    return [tweet for tweet in tweets]


def get_clean_tweets_txt(nome_base, colecao):
    """Carrega os tweets limpos."""
    cliente = get_client()
    colecao = load_database(cliente, nome_base, colecao)
    tweets = colecao.find()
    lista_tweets = []
    for tweet in tweets:
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
        except KeyError:
            full_tweet = tweet['text']
        if len(full_tweet) < 1:
            continue
        lista_tweets.append(pre_processing.clean_text(full_tweet))
    cliente.close()
    return lista_tweets


def get_tweets_txt(nome_base, colecao):
    """Get text from tweets without clean."""
    cliente = get_client()
    colecao = load_database(cliente, nome_base, colecao)
    tweets = colecao.find()
    lista_tweets = []
    for tweet in tweets:
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
        except KeyError:
            full_tweet = tweet['text']
        if len(full_tweet) < 1:
            continue
        lista_tweets.append(full_tweet)
    cliente.close()
    return lista_tweets
