# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central Estrutural -
Sara - Sistema de Análise de Dados com Redes Complexas e Analytics
Focado em análises politicas no twitter.
Realiza o calculo de centralidade
"""
import sys

import networkx as nx

import sara.core.centralidade as relevante


class Importancia():
    """docstring for Estrutural."""

    def __init__(self):
        try:
            self.nome_base = sys.argv[1]
            self.nome_colecao = sys.argv[2]
            self.nome_rede = sys.argv[3]
            self.lista_nos = ""
        except IndexError as exc:
            print(f"ERRO {exc}!!"
                  "Digite : \n>python3 sara_centralidade.py"
                  " <nome_base> <nome_colecao> <grafo>")
            sys.exit()

    def carrega_grafo(self):
        """carrega um grafo e gera uma lista de vértices"""
        rede = nx.read_gml(self.nome_rede)
        self.lista_nos = rede.nodes()

    def realiza_busca(self):
        """realiza pesquisa na rede."""
        # self.lista_nos=["biakicis","mblivre","SenadorKajuru",
        # "joaoamoedonovo","QuebrandoOTabu","BolsonaroSP",
        # "CarlosBolsonaro",
        # "jose_neumanne","davialcolumbre"]
        # self.lista_nos=['mblivre',"biakicis","jose_neumanne"]
        nome_rede = self.nome_rede.split(".")[0]
        relevante.main(self.nome_base, self.nome_colecao,
                       self.lista_nos, nome_rede)


if __name__ == '__main__':
    importancia = Importancia()
    importancia.carrega_grafo()
    importancia.realiza_busca()
