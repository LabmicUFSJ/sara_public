# -*- coding: utf-8 -*-
"""
Inicia uma conexão com o twitter..
Remova as credencias ao realizar um upload para o git.
"""
import twitter


def inicia_conexao():
    """Abre a conexão com a api do twitter"""
    api = twitter.Api(
        consumer_key='YOUR consumer_key',
        consumer_secret='YOUR consumer_secret',
        access_token_key='YOUR access_token_key',
        access_token_secret='YOUR access_token_secret',
        sleep_on_rate_limit=True,
        tweet_mode='extended',
    )
    return api

