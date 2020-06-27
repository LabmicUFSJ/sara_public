# -*- coding: utf-8 -*-
"""
Framework de Análise de dados Politicos no twitter..
Central de Coleta Dados do Framework de Análise de Dados -
Sara - Sistema de Análise de Dados com Redes Complexas e Analytics
Focado em análises politicas no twitter.

Coletor API
"""
import sys

from sara.core.sauron_coletor import Sauron
from sara.core.logger import log
# padrao_pesquisa,limite,colecao,nome_banco="eleicao"
# coletor de dados


# termo="haddad"
# n_tweets=0
# colecao="haddad_2310"
# nome_banco="eleicao"

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
