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
    name_file = sys.argv[0]
    termo = sys.argv[1]
    n_tweets = sys.argv[2]
    colecao = sys.argv[3]
    nome_banco = sys.argv[4]
except IndexError as exc:
    print(f"error {exc}")
    print(f"ERRO!Digite {name_file} <termo> "
          "<numero_tweets> <colecao> <banco de dados>")
    print("\nTermo: O termo a ser coletado" +
          "\nNúmero de Tweets: número de tweets a ser coletado." +
          "0 para definir sem limites" +
          "\nColecao: A coleção onde os tweets serão salvos." +
          "\nBanco de Dados: O  banco onde os dados serão armazenados")

    sys.exit()


log(termo)
coletor = Sauron()
coletor.pesquisa(termo, n_tweets, colecao, nome_banco)

# odetalhista.detector_bots(nome_banco,colecao)
