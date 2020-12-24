# -*- coding: utf-8 -*-
"""
Coletor de Tweets.

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
"""
import sys

from sara.core.collector import SaraCollector
from sara.core.logger import log
from sara.core.sara_data import SaraData

# termo colecao numero_tweets
try:
    name = sys.argv[0]
    term = sys.argv[1]
    n_tweets = sys.argv[2]
    collection = sys.argv[3]
except IndexError as exc:
    print(f"error {exc}\n")
    print(f"ERRO!Digite {name} <termo> "
          "<numero_tweets> <colecao>")
    print('\n--------------------------------------------\n')
    print("Termo: O termo a ser coletado" +
          "\nNúmero de Tweets: número de tweets a ser coletado." +
          " 0 para definir sem limites" +
          "\nColecao: A coleção onde os tweets serão armazenados.\n")

    sys.exit()


log(term)
storage = SaraData(collection)
data_collector = SaraCollector(storage)
data_collector.real_time_collector(term, n_tweets)
