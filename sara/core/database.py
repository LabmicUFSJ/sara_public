# -*- coding: utf-8 -*-
"""
Realiza a conexao com o MOngoDB
"""
from pymongo import MongoClient

# import processamento.pre_processamento as pre_processamento


def inicia_conexao():
    """Inicia a conexão com o mongoDb"""
    cliente = MongoClient()
    cliente = MongoClient('localhost', 27017)
    return cliente


def carregar_banco(cliente, nome, colecao):
    """Carrega um banco com uma colecao"""
    banco = cliente[nome]
    return banco[colecao]


def carregar_usuarios(nome_banco, colecao):
    """Carrega e retorna uma lista de usuários"""
    cliente = inicia_conexao()
    colecao = carregar_banco(cliente, nome_banco, colecao)
    usuarios = colecao.find({}, {"user": 1})
    lista_usuarios = []
    for usuario in usuarios:
        lista_usuarios.append(usuario.get('user'))
    return lista_usuarios


def carrega_tweets(nome_banco, colecao):
    """Carrega Tweets."""
    cliente = inicia_conexao()
    colecao = carregar_banco(cliente, nome_banco, colecao)
    tweets = colecao.find({})
    lista_tweets = []
    for tweet in tweets:
        lista_tweets.append(tweet)
    return lista_tweets


def carrega_tweet_mongo(nome_base, colecao):
    """Carrega os tweets limpos."""
    cliente = inicia_conexao()
    colecao = carregar_banco(cliente, nome_base, colecao)
    tweets = colecao.find({})
    lista_tweets = []
    for tweet in tweets:
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
            if len(full_tweet) > 1:
                lista_tweets.append(full_tweet)
        # pylint: disable=broad-except
        except (KeyError, Exception):
            pass
    return lista_tweets
