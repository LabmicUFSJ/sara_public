# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
LDA
"""
# import os
# from pprint import pprint

import sara.core.cloud as cloud
import sara.core.pre_processamento as pre_processamento
import gensim
import gensim.corpora as corpora
import sara.core.database as bd
import nltk
# from gensim.models import CoherenceModel
# from gensim.utils import simple_preprocess
# from nltk.stem import RSLPStemmer


def make_bigrams(bigram_mod, texts):
    """Gera bigrama dos textos."""
    return [bigram_mod[doc] for doc in texts]


def unpack_tupla(tupla):
    """unpack_tupla"""
    (word1, word2) = tupla
    final = word1 + " " + word2
    return final


def carrega_tweet_mongo(banco, colecao):
    """Carrega e realiza a chamada de limpeza dos tweets"""
    print(banco, colecao)
    cliente = bd.inicia_conexao()

    # nome termo,collection
    colecao = bd.carregar_banco(cliente, banco, colecao)
    tweets = tweets = colecao.find({})
    lista_tweets = []
    for tweet in tweets:
        # print(tweet)
        try:
            full_tweet = tweet["extended_tweet"]["full_text"]
            if len(full_tweet) > 1:
                lista_tweets.append(
                    pre_processamento.pre_processing(full_tweet)
                )
        except Exception:
            # print("erro",e)
            pass
    # print(len(lista_tweets))
    return lista_tweets


def main(banco, colecao, n_topicos):
    tweets = carrega_tweet_mongo(banco, colecao)
    # print("tweets2", len(tweets))
    # exit()
    docfinal = []

    # bigramas
    for doc in tweets:
        nltk_tokens = nltk.word_tokenize(doc)
        docfinal.append(list(nltk.bigrams(nltk_tokens)))
        # docfinal.append(doc.split())
    l_final = []
    # combina os bigramas em conjunto de palavras.
    for i in docfinal:
        # print(i)
        lista = []
        for elementos in i:
            # print(elementos)
            lista.append(unpack_tupla(elementos))
        l_final.append(lista)
    # print(l_final)
    docfinal = l_final

    # #Stemização no texto
    # st = RSLPStemmer()
    # doc_stemming=[]
    # for i in docfinal:
    #     list=[]
    #     for k in i:
    #         list.append(st.stem(k))
    #     doc_stemming.append(list)
    # docfinal=doc_stemming
    # ------------------

    # Creating the term dictionary of our courpus,
    # where every unique term is assigned an index.
    # dictionary = corpora.Dictionary(doc_clean)
    dictionary = corpora.Dictionary(docfinal)
    # Converting list of documents (corpus) into Document Term Matrix
    # using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in docfinal]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # hdp = HdpModel(doc_term_matrix,dictionary, T=200)
    #
    # def topic_prob_extractor(gensim_hdp):
    #     shown_topics = gensim_hdp.show_topics(num_topics=-1, formatted=False)
    #     topics_nos = [x[0] for x in shown_topics ]
    #     weights = [ sum([item[1] for item in shown_topics[topicN][1]]) for topicN in topics_nos ]
    #
    #     return pd.DataFrame({'topic_id' : topics_nos, 'weight' : weights})
    #
    # print(topic_prob_extractor(hdp))

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(
        corpus=doc_term_matrix,
        id2word=dictionary,
        num_topics=10,
        random_state=1000,
        update_every=1,
        chunksize=1000,
        passes=100,
        alpha='auto',
        per_word_topics=True,
    )

    topicos = ldamodel.top_topics(
        corpus=doc_term_matrix,
        dictionary=dictionary,
        coherence='u_mass',
        topn=10,
        processes=-1,
    )
    final = []
    # print("TOpicos", topicos)
    for top in topicos:
        # print(top)
        final.append(top[0])

    lf = []
    for i in final:
        # print("Topicos:",i)
        for k in i:
            lf.append(k)
    # print(lf)
    cloud.cloud_lda(lf, n_topicos)
    return lf
