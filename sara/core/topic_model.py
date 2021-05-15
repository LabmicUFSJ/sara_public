# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""Topic Model"""


import gensim
import gensim.corpora as corpora
import nltk


def unpack_tupla(tupla):
    """Unpack_tupla"""
    (word1, word2) = tupla
    word = word1 + " " + word2
    return word


# pylint:disable=too-many-locals
def get_lda_topics(tweets, n_topics):
    """Get LDA topics."""
    docfinal = []
    # bigrams
    for doc in tweets:
        nltk_tokens = nltk.word_tokenize(doc)
        docfinal.append(list(nltk.bigrams(nltk_tokens)))
    l_final = []
    # combina os bigramas em conjunto de palavras.
    for i in docfinal:
        lista = [unpack_tupla(elementos) for elementos in i]
        l_final.append(lista)
    docfinal = l_final

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

    topics = ldamodel.top_topics(corpus=doc_term_matrix,
                                 dictionary=dictionary, coherence='u_mass',
                                 topn=10, processes=-1)
    top_topics = [top[0] for top in topics]
    topics = []
    for l_topic in top_topics:
        for topic in l_topic:
            topics.append(topic)
    return topics, n_topics
