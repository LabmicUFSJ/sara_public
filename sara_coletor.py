# -*- coding: utf-8 -*-
"""
Coletor de Tweets.

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
"""
import sys

from sara.core.sauron_coletor import Sauron
from sara.core.logger import log


# termo colecao numero_tweets
try:
    name = sys.argv[0]
    term = sys.argv[1]
    n_tweets = sys.argv[2]
    collection = sys.argv[3]
    database = sys.argv[4]
except IndexError as exc:
    print(f"error {exc}")
    print(f"ERRO!Digite {name} <termo> "
          "<numero_tweets> <colecao> <banco de dados>")
    print("\nTermo: O termo a ser coletado" +
          "\nNúmero de Tweets: número de tweets a ser coletado." +
          "0 para definir sem limites" +
          "\nColecao: A coleção onde os tweets serão salvos." +
          "\nBanco de Dados: O  banco onde os dados serão armazenados")

    sys.exit()


log(term)
data_collector = Sauron()
data_collector.pesquisa(term, n_tweets, collection, database)
