# -*- coding: utf-8 -*-
# !/usr/bin/env python3

"""Pre-processing Class."""
# import ast
import os
import re
# import base
import string
from unicodedata import normalize

import emoji
import spacy

import sara.stopwords.StopWords as stopWords

absolute_path = os.path.dirname(os.path.abspath(__file__))


def _remove_emoji(text):
    """Remove Emoji from text."""
    return emoji.get_emoji_regexp().sub(u'', text)


def _remove_accents(txt):
    """Remove accents."""
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def _remove_user_mention(text):
    """Remove user mention, @username."""
    if re.search(r"(@)\S*", text):
        return re.sub(r"(@)\S*", " ", text)
    return text


def _remove_links(text):
    """Remove links."""
    text = re.sub(r"(pic.twitter)\S*", " ", text)
    if re.search(r"(https:)\S*", text):
        text = re.sub(r"(https:)\S*", " ", text)
        return text.replace("...", "")
    if re.search(r"(http:)\S*", text):
        return re.sub(r"(http:)\S*", " ", text)
    return text


class PreProcessing:
    """Classe responsável pelo pré-processamento dos dados."""

    def __init__(self, remove_adjectives=False):
        """pre-processing."""
        self.nlp = spacy.load("pt_core_news_sm")
        self.spacy_stopwords = spacy.lang.pt.stop_words.STOP_WORDS
        path_to_stopwords = (f"{absolute_path}/"
                             "../stopwords/stopwords_txt/stopwords_v2.txt")
        self.set_stop = stopWords.load_stop_words(path_to_stopwords)

        if remove_adjectives:
            # Load adjectives
            path_adjectives = (f"{absolute_path}/"
                               "../stopwords/stopwords_txt/adjetivos.txt")
            self.set_adjectives = stopWords.load_stop_words(path_adjectives)
            self.set_stop = self.set_stop.union(self.set_adjectives)
        # Merge stopWords set
        self.set_stop = self.set_stop.union(self.spacy_stopwords)

    def add_stop_word(self, word):
        """Add a stop word to set the stopwords."""
        self.set_stop.add(word)

    def get_stowords(self):
        """Get a set with all stopwords used."""
        return self.set_stop

    def clean_texts(self, words):
        """Clean list with multiple text."""
        return [self.clean_text(word) for word in words]

    def clean_text(self, text):
        """Clean a text."""
        if not isinstance(text, str):
            raise TypeError('Only string has accept.'
                            f'Our send: {text.__class__}')
        # convert text to lowercase
        text = text.lower()
        # remove emoji
        # text = self.__remove_emoji(text)
        # find links
        text = _remove_links(text)
        # remove user mention
        text = _remove_user_mention(text)
        # remove number in text
        text = re.sub(r"\d+", " ", text)
        # remove smiles type kkk
        text = re.sub(r"(kk)+", " ", text)
        # remove broken words
        text = re.sub(r"\s[\w]{1}\s", " ", text)
        # remove punctuation
        text = re.sub('[' + string.punctuation + ']', " ", text)
        # White spaces removal
        text = text.strip()
        # remove accents
        text = _remove_accents(text)
        # generate tokens
        token_list = []
        tokens = self.nlp(text)
        for token in tokens:
            word = re.sub(r"\s", "", token.text)
            if len(word) < 2:
                continue
            token_list.append(word)
        # remove stopwords
        tokens_final = [tk for tk in token_list if tk not in self.set_stop]
        return " ".join(tokens_final)
