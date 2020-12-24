# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central de Análise de conteúdo do Framework Sara.
Gera a Nuvem de palavras

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
"""
# import core.bagwords as bagwords
import sys

from sara.core.pre_processing import PreProcessing
from sara.core.topic_model import get_lda_topics
from sara.core.sara_data import SaraData

try:
    name = sys.argv[0]
    collection = sys.argv[1]
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Digite {name} <colecao>")
    sys.exit(-1)

data = SaraData(collection, storage_type='mongodb')
projection = {'text':1,
              'extended_tweet.full_text':1,
              'retweeted_status.text':1,
              'retweeted_status.extendeted_tweet.full_text':1}
tweets = data.get_projected_data(projection, 0)

print(f"Colecao a ser utilizada: {collection}")

processing = PreProcessing()
full_tweets = []
for i in tweets:
    full_text = None
    if 'text' in i:
        full_text = i.get('text')
    if 'extended_tweet' in i:
        full_text = i['extended_tweet']['full_text']
    if 'retweeted_status' in i:
        retweeted = i.get('retweeted_status')
        full_text = retweeted['text']
        if 'extended_tweet' in retweeted:
            full_text = retweeted['full_text']
    if full_text is not None:
        full_tweets.append(processing.clean_text(full_text))
print(full_tweets)
# Análise de conteúdo
words = get_lda_topics(full_text, 10)
# print("Modelagem ... OK\nSentimento Modelagem:")
# print("Sentimento Modelagem... ok")
