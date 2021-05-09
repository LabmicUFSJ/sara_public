# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Load stopWords
"""


def load_stop_words(words):
    """Load stopwords list, return a set"""
    with open(words, "r") as lines:
        set_stop_words = set()
        for i in lines:
            set_stop_words.add(i.strip())
    return set_stop_words
