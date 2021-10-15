"""Script to make TF-IDF analysis.

SARA
Licença - MIT
LabMIC - UFSJ
2019 - 2021
"""
import sys

from sara.core.pre_processing import PreProcessing
from sara.core.sara_data import SaraData
from sara.core.tf_idf import get_tf_idf

try:
    file_name = sys.argv[0]
    collection = sys.argv[1]
    database = sys.argv[2]
except IndexError as exc:
    print(f"error {exc}\n")
    print(f"ERRO!Please input {file_name} <collection> <database>")
    print('\n--------------------------------------------\n')
    sys.exit(-1)


def main():
    """Make TF-IDF analysis."""
    processing = PreProcessing()
    storage = SaraData(collection, database)
    projection = {'text': 1,
                  'extended_tweet.full_text': 1,
                  'retweeted_status.text': 1,
                  'retweeted_status.extended_tweet.full_text': 1}
    tweets = storage.get_projected_data(projection, 0)
    tweets_text = []
    for i in tweets:
        text = i.get('text')
        if 'extended_tweet' in i:
            text = i.get('extended_tweet')['full_text']
        if 'retweeted_status' in i:
            retweeted = i.get('retweeted_status')
            text = retweeted.get('text')
            extended = retweeted.get('extended_tweet')
            if extended:
                text = extended.get('full_text')
        if text and len(text) > 2:
            text_clean = processing.clean_text(text)
            text = None
            if len(text_clean) > 2:
                tweets_text.append(text_clean)
    get_tf_idf(tweets_text)


if __name__ == '__main__':
    main()
