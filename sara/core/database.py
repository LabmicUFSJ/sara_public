# -*- coding: utf-8 -*-
"""
Realiza a conexao com o MongoDB.
MongoDB utils.
"""
from pymongo import MongoClient

from sara.core.pre_processing import pre_processing
import random

# import processamento.pre_processamento as pre_processamento


def inicia_conexao():
    """Inicia a conexão com o mongoDb."""
    return MongoClient('localhost', 27017)


def _load_database(client, name, collection):
    """Carrega um banco com uma colecao."""
    database = client[name]
    return database[collection]


def load_users(database_name, collection, number_users):
    """
    Carrega e retorna uma lista de usuários.
    Return a list not duplicated the users.
    """
    client = inicia_conexao()
    collection = _load_database(client, database_name, collection)
    total_documents = collection.count_documents({})
    consult_number = total_documents if number_users is None else number_users
    users = collection.find({}, {"user": 1}).limit(consult_number*2)
    users_dict = {}
    for user in users:
        user_id = user['user']['id']
        users_dict[user_id] = user['user']
    print(f"Número de usuários unicos recuperados: {len(users_dict)}")
    unique_users = len(users_dict) if number_users is None else number_users
    client.close()
    return random.sample(list(users_dict.values()), k=unique_users)


def return_users(database_name, collection, users_id):
    client = inicia_conexao()
    cursor = _load_database(client, database_name, collection)
    users = [cursor.find({"user.id_str": usr_id}
                         )[0]['user'] for usr_id in users_id]
    client.close()
    return users


def carrega_tweets(nome_banco, colecao, limite=None):
    """
    Carrega Tweets.
    Return a tweet list.
    """
    cliente = inicia_conexao()
    colecao = _load_database(cliente, nome_banco, colecao)
    if limite:
        tweets = colecao.find().limit(limite)
    tweets = colecao.find()
    lista_tweets = []
    cliente.close()
    for tweet in tweets:
        lista_tweets.append(tweet)
    return lista_tweets


def load_full_tweets_clean(nome_base, colecao):
    """Carrega os tweets limpos."""
    cliente = inicia_conexao()
    colecao = _load_database(cliente, nome_base, colecao)
    tweets = colecao.find()
    lista_tweets = []
    for tweet in tweets:
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
        except KeyError:
            # print(f"Error loadind extended tweet: {exc}")
            # try load tweet.
            full_tweet = tweet['text']
        if len(full_tweet) < 1:
            continue
        lista_tweets.append(pre_processing(full_tweet))

    return lista_tweets
