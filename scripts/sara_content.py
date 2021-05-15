# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Script to perform content analisys.
SARA
LabMIC - UFSJ
Carlos Barbosa
"""
import sys

import sara.core.cloud as cloud
from sara.core.pre_processing import PreProcessing
from sara.core.sara_data import SaraData
from sara.core.topic_model import get_lda_topics

try:
    name = sys.argv[0]
    collection = sys.argv[1]
except IndexError as exc:
    print(f"Erro: {exc}")
    print(f"Use python {sys.argv[0]} <collection_name>")
    sys.exit(-1)

data = SaraData(collection, storage_type='mongodb')
projection = {'text': 1,
              'extended_tweet.full_text': 1,
              'retweeted_status.text': 1,
              'retweeted_status.extendeted_tweet.full_text': 1}
tweets = data.get_projected_data(projection, 0)

print(f"Collection: {collection}")


def main():
    """Execute content analysis"""
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
            text_cleaned = processing.clean_text(full_text)
            if len(text_cleaned) > 2:
                full_tweets.append(text_cleaned)
    print('Full text', full_tweets)
    # Topic model
    topics, n_topics = get_lda_topics(full_tweets, 10)
    # Show the result as a word cloud.
    cloud.cloud_lda(topics, n_topics)


if __name__ == "__main__":
    main()
