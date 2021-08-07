# -*- coding: utf-8 -*-
"""
Script to collect real time tweets.

Sara - Framework
Licença - MIT
Carlos Magno
LabMIC - UFSJ
"""
import sys

from sara.core.collector import SaraCollector
from sara.core.logger import log
from sara.core.sara_data import SaraData


try:
    name = sys.argv[0]
    term = sys.argv[1]
    n_tweets = sys.argv[2]
    collection = sys.argv[3]
except IndexError as exc:
    print(f"error {exc}\n")
    print(f"ERRO!Digite {name} <term> "
          "<tweets_number> <collection>")
    print('\n--------------------------------------------\n')
    print("Term: The term will be collected" +
          "\ntweets_limit: Number of tweets will be collected." +
          " 0 - not set a limit to collect." +
          "\nCollection: Collection where these tweets will be stored.\n")

    sys.exit(-1)


if __name__ == '__main__':
    log(term)
    storage = SaraData(collection)
    data_collector = SaraCollector(storage)
    data_collector.real_time_collector(term, n_tweets)
