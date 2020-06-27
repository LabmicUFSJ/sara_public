# -*- coding: utf-8 -*-
"""
Coletor Web
Realiza a coleta dos comentários associados a determinado
Tweet.

Utiliza o selenium
- Necessário instalação de arquivo externo chromedriver
"""

import sys

import coletor_web.coletor_comentarios as comment
import core.database as db


def main(banco_dados, colecao):
    """Coletor web"""
    cliente = db.inicia_conexao()
    conector = db.carregar_banco(cliente, banco_dados, colecao)
    tweets = conector.find({})

    for tweet in tweets:
        id_tweet = tweet['id_str']
        usuario_tweet = tweet['user']['screen_name']
        try:
            comment.get_data(usuario_tweet, id_tweet)
        # pylint: disable= broad-except
        except Exception as exc:
            print("A coleta foi encerrada.")
            print(f"Erro {exc}")
            sys.exit()


if __name__ == '__main__':
    try:
        name_file = sys.argv[0]
        database = sys.argv[1]
        collection = sys.argv[2]
    except IndexError as exc:
        print(f"erro {exc}")
        print(f"Digite {name_file} <banco> <colecao>")
        sys.exit()
    main(database, collection)
