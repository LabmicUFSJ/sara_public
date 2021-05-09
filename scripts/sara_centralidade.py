# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central Estrutural -
Realiza o calculo de centralidade

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
"""
import sys

import networkx as nx

import sara.core.centrality as centrality_measures


class Importance():
    """Centrality."""

    def __init__(self):
        try:
            self.database = sys.argv[1]
            self.collection = sys.argv[2]
            self.network_name = sys.argv[3]
            self.nodes = ""
        except IndexError as exc:
            print(f"ERRO {exc}!!"
                  "Digite : \n>python3 sara_centralidade.py"
                  " <nome_base> <nome_colecao> <grafo>")
            sys.exit()

    def load_graph(self):
        """carrega um grafo e gera uma lista de vértices."""
        graph = nx.read_gml(self.network_name)
        self.nodes = graph.nodes()

    def search(self):
        """realiza pesquisa na rede."""
        network = self.network_name.split(".")[0]
        centrality_measures.main(self.database, self.collection,
                                 self.nodes, network)


if __name__ == '__main__':
    importance = Importance()
    importance.load_graph()
    importance.search()
