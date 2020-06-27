# -*- coding: utf-8 -*-
# need this if you want to save tfidf_matr
# explorar usar tf-id
"""
TF-idf
"""

from sklearn.feature_extraction.text import TfidfVectorizer

import sara.core.cloud as cloud
import sara.core.database as bd
from sara.core.pre_processamento import pre_processamento


def carrega_tweet_mongo(nome_base, colecao):
    """Carrega e realiza a chamada de limpeza dos tweets"""
    cliente = bd.inicia_conexao()
    colecao = bd.carregar_banco(cliente, nome_base, colecao)
    tweets = tweets = colecao.find({})
    lista_tweets = []
    for tweet in tweets:
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
            if len(full_tweet) > 1:
                lista_tweets.append(
                    pre_processamento(full_tweet)
                )
        except Exception:
            pass
    return lista_tweets


# for i in lista_tweets:
#     print(i)
# #limiar minimo para selecionar o topico
limiar = 0.001
topicos_validos = []


def completo(lista):
    """
    Combina as strings
    """
    string = ""
    for i in lista:
        string += i + " "
    return [string]


def getkey(item):
    return item[1]


def main(banco, colecao):
    lista_tweets = carrega_tweet_mongo(banco, colecao)
    # Encontra as palavras mais relevantes usando abordagem de tf-idf
    doc_completo = completo(lista_tweets)
    tf = TfidfVectorizer(lista_tweets)
    tfidf_matrix = tf.fit_transform(doc_completo)
    # corpus
    feature_names = tf.get_feature_names()
    doc = 0
    feature_index = tfidf_matrix[doc, :].nonzero()[1]
    tfidf_scores = zip(
        feature_index, [tfidf_matrix[doc, x] for x in feature_index]
    )

    final = []
    l_limiar = []
    for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
        final.append((w, s))

    print(len(l_limiar))
    last = sorted(final, key=getkey, reverse=True)

    for i in last:
        if float(i[1]) > limiar:
            retorno = pre_processamento.pre_processamento(i[0])
            if len(retorno) > 1:
                if float(i[1]) > 0.01:
                    # print(i,"Cloud:",i)
                    topicos_validos.append(i)

    print(len(topicos_validos))
    cloud.cloud_tf(topicos_validos, 100)
    return topicos_validos
