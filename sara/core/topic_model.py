# -*- coding: utf-8 -*-
"""Topic Model

Topic model with Gensin and Scikit-learn

This code is inspired by the code writed by:

# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
# License: BSD 3 clause
# https://scikit-learn.org/

In additional this code uses the changes made by:
Lucas Félix - lucasgsfelix
Vinícius Vieira - vfvieira
"""


import uuid

import gensim
import matplotlib.pyplot as plt
import nltk
from gensim import corpora
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sara.core.utils import create_path


# pylint:disable=too-many-locals
def plot_top_words(model, feature_names, number_topics, title, color):
    """Plot list with topics."""
    figure_distribution = {1: (1, 1), 2: (1, 2),
                           3: (1, 3), 4: (1, 4),
                           5: (1, 5), 6: (2, 3),
                           7: (2, 4), 8: (2, 4),
                           9: (2, 5), 10: (2, 5)}
    try:
        rows, columns = figure_distribution[number_topics]
    except KeyError as error:
        print(f"Error: {error}, The max topics to plot is 10"
              f"the value passed is {number_topics}")
        return

    fig, axes = plt.subplots(rows, columns, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-number_topics - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        position = axes[topic_idx]
        position.barh(top_features, weights, height=0.7, color=color)
        position.set_title(f'Tópico {topic_idx +1}',
                           fontdict={'fontsize': 15})
        position.invert_yaxis()
        position.tick_params(axis='both', which='major', labelsize=12)
        for i in 'top right left'.split():
            position.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=25)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    # plt.show()
    create_path("resultados/topic_model/")
    save_name = f"resultados/topic_model/{title}_{str(uuid.uuid4().hex)}.pdf"
    print(f"Saving file in the path {save_name}")
    fig.savefig(save_name)


def _unpack_tupla(tupla):
    """Unpack_tupla"""
    (word1, word2) = tupla
    return word1 + " " + word2


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
        lista = [_unpack_tupla(elementos) for elementos in i]
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


def generate_tf_idf(corpus, n_features=1000, bigram=False):
    """Generate TF-idf bag-of-words."""
    ngram_interval = (1, 1)
    if bigram:
        # to use only bigram change to (2, 2)
        ngram_interval = (1, 2)
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=1,
                                       max_features=n_features,
                                       ngram_range=ngram_interval)
    tfidf = tfidf_vectorizer.fit_transform(corpus)

    return tfidf_vectorizer, tfidf


def generate_tf(corpus, n_features=1000, bigram=False):
    """Generate TF vectorization."""
    # set to use unigram or bigram
    ngram_interval = (1, 1)
    if bigram:
        ngram_interval = (1, 2)
    # generate term-frequency representation
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=1,
                                    max_features=n_features,
                                    ngram_range=ngram_interval)

    term_frequency = tf_vectorizer.fit_transform(corpus)
    return tf_vectorizer, term_frequency


def lda_scikit(corpus, n_components=10, bigram=False):
    """Run LDA topic model using Scikit-learn"""
    tf_vectorizer, term_frequency = generate_tf(corpus, bigram=bigram)
    lda = LatentDirichletAllocation(n_components=n_components, max_iter=10,
                                    learning_method='online',
                                    learning_offset=50,
                                    random_state=0)
    lda.fit(term_frequency)
    tf_feature_names = tf_vectorizer.get_feature_names()

    return lda, tf_feature_names


def nmf_scikit(corpus, n_components=10, bigram=False):
    """Run NMF topic model analysis using Scikit learn."""
    tfidf_vectorizer, tfidf = generate_tf_idf(corpus, bigram=bigram)
    nmf = NMF(n_components=n_components, random_state=1, max_iter=1600,
              alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    return nmf, tfidf_feature_names
