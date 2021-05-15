# -*- coding: utf-8 -*-
"""
Modulo de coleta utilizando a api do Twitter .
"""

import sys
import time

from requests.exceptions import ChunkedEncodingError
from twitter.error import TwitterError
from urllib3.exceptions import IncompleteRead, ProtocolError

from sara.core.logger import log_erro
from sara.core.sara_data import SaraData
from sara.credentials.twitter_api import get_twitter_api


class SaraCollector():
    """Class responsible for collecting the Tweets."""

    def __init__(self, storage):
        # Get twitter API
        self.api = get_twitter_api()
        self.show_data_treshold = 1000
        self.sleep_on_error = 10
        if not isinstance(storage, SaraData):
            raise TypeError('The Storage type must be SaraData. But the '
                            f'storage type is: {type(storage).__name__} .')
        self.storage = storage

    def scheduled(self, monitored_term, duration):
        """Collect tweets in real time in scheduled mode."""
        tweets = self.api.GetStreamFilter(track=[monitored_term])
        number_tweets_collected = 0
        exhibition_count = 0
        now = time.time()
        break_after = (duration*60) + now
        try:
            for tweet in tweets:
                if time.time() >= break_after:
                    print(f"Collected tweets {number_tweets_collected}")
                    return
                if exhibition_count == self.show_data_treshold:
                    print(f"Collected tweets {number_tweets_collected}")
                    exhibition_count = 0
                number_tweets_collected += 1
                exhibition_count += 1
                # coloca na fila para processamento dos dados
                self.storage.save_data((tweet))
        except (TwitterError, ProtocolError, IncompleteRead,
                ChunkedEncodingError) as exc:
            print(f"error {exc.message}")
            log_erro(exc.message)
            if 'Unauthorized' in exc.message:
                print(f"Please check your credentials {exc.message}.")
                sys.exit(-1)

            # Wait X seconds to try to collect new tweets again.
            time.sleep(self.sleep_on_error)
            # realiza coleta no período de tempo restante
            restante = break_after-time.time()
            self.scheduled(monitored_term, restante)

    def real_time_collector(self, monitored_term, collection_limit=0):
        """Collect tweets in real time mode."""
        tweets = self.api.GetStreamFilter(track=[monitored_term])
        print(f"Running real time collector, monitored term: {monitored_term}")
        number_tweets_collected = 0
        exhibition_count = 0
        try:
            for tweet in tweets:
                if exhibition_count == self.show_data_treshold:
                    print(f"Collected tweets {number_tweets_collected}")
                    exhibition_count = 0
                number_tweets_collected += 1
                exhibition_count += 1
                self.storage.save_data((tweet))
                if collection_limit != 0:
                    if number_tweets_collected == collection_limit:
                        print("Limit the collect reached.")
                        return
        except (TwitterError, ProtocolError, IncompleteRead,
                ChunkedEncodingError) as exc:
            print(f"error {exc.message}")
            log_erro(exc.message)
            if 'Unauthorized' in exc.message:
                print(f"Please check your credentials {exc.message}.")
                sys.exit(-1)
            # wait to retry collect tweets.
            time.sleep(self.sleep_on_error)
            self.real_time_collector(monitored_term, collection_limit)

    def collector_followers(self, user_id):
        """Collect followers from user id."""
        next_cursor = -1
        new_list = []
        while True:
            data = self.api.GetFollowersPaged(user_id=user_id,
                                              cursor=next_cursor)
            next_cursor, _, users = data
            new_list = list(set(new_list+users))
            if len(users) < 200:
                break
        name = str(user_id)+'.json'
        for user in new_list:
            self.storage.save_data_file(name, user.AsDict())
