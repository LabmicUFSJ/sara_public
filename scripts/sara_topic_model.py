"""
Running topic model with SARA
Add an example Running topic model.

"""

from sara.core.pre_processing import PreProcessing
from sara.core.sara_data import SaraData
from sara.core.topic_model import lda_scikit, plot_top_words

# try:
#     database = sys.argv[1]
#     collection = sys.argv[2]
# except IndexError as error:
#     print(f"Error {error}")
#     print("Please input, python3 sys.argv[0] <database>
# <collection> <title>")


def _get_text_retweet(retweet):
    """Return text of retweet."""
    retweeted = retweet['retweeted_status']
    full_text = retweeted['text']
    if retweeted.get('extended_tweet'):
        return retweeted['extended_tweet'].get('full_text', full_text)
    return full_text


def get_full_text(tweet):
    """Return a list of full text from tweets."""
    full_text = tweet.get('text')
    if tweet.get('retweeted_status'):
        full_text = _get_text_retweet(tweet)
        return full_text
    if tweet.get('extended_tweet'):
        extended_tweet = tweet.get('extended_tweet')
        full_text = extended_tweet.get('full_text', full_text)
        return full_text
    return full_text


def main(collection, database):
    """Run topic model."""

    processing = PreProcessing()
    storage = SaraData(collection, database)
    tweet_filter = {"lang": "pt"}
    projection = {'text': 1,
                  'extended_tweet.full_text': 1,
                  'retweeted_status.text': 1,
                  'retweeted_status.extended_tweet.full_text': 1}

    # Recupera tweets do banco, essa parte poderia ser substituida por uma
    # consulta direto no MongoDB
    tweets = storage.get_filtered_tweet(tweet_filter, projection, 0)

    # Extrai o texto dos tweets
    raw_texts = list(map(get_full_text, tweets))

    # Limpa o texto
    cleaned_texts = list(map(processing.clean_text, raw_texts))

    # realiza a modelagem de tópicos
    model_lda, names = lda_scikit(cleaned_texts, 10, bigram=True)

    # Exibe os tópicos
    plot_top_words(model_lda, names, 10, "Modelagem de Tópicos", "blue")


if __name__ == '__main__':

    # Database name
    DATABASE = ""
    # Collection Name
    COLLECTION = ""
    main(COLLECTION, DATABASE)
