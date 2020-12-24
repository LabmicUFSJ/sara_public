# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""LDA"""
# import os
# from pprint import pprint

import gensim
import gensim.corpora as corpora
import nltk

import sara.core.cloud as cloud


def make_bigrams(bigram_mod, texts):
    """Gera bigrama dos textos."""
    return [bigram_mod[doc] for doc in texts]


def unpack_tupla(tupla):
    """unpack_tupla"""
    (word1, word2) = tupla
    final = word1 + " " + word2
    return final


# pylint:disable=too-many-locals
def get_lda_topics(tweets, n_topicos):
    """Get LDA topics."""
    docfinal = []
    # bigramas
    for doc in tweets:
        nltk_tokens = nltk.word_tokenize(doc)
        print(nltk_tokens)
        docfinal.append(list(nltk.bigrams(nltk_tokens)))
    l_final = []
    # combina os bigramas em conjunto de palavras.
    for i in docfinal:
        lista = [unpack_tupla(elementos) for elementos in i]
        l_final.append(lista)
    docfinal = l_final

    # print(docfinal)
    # Creating the term dictionary of our courpus,
    dictionary = corpora.Dictionary(docfinal)
    # Converting list of documents (corpus) into Document Term Matrix
    # using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in docfinal]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(corpus=doc_term_matrix, id2word=dictionary, num_topics=10,
                   random_state=1000, update_every=1, chunksize=1000,
                   passes=100, alpha='auto', per_word_topics=True)

    topicos = ldamodel.top_topics(corpus=doc_term_matrix,
                                  dictionary=dictionary, coherence='u_mass',
                                  topn=10, processes=-1)
    final = [top[0] for top in topicos]
    topics = []
    for i in final:
        for k in i:
            topics.append(k)
    cloud.cloud_lda(topics, n_topicos)
    return topics
