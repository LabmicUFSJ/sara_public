# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Script to make centrality analysis

This script uses the SaraFramework.

SARA Framework
License - MIT
LABMIC - UFSJ - 2019-2021
Carlos Barbosa
"""
import sys

import networkx as nx

import sara.core.centrality as centrality_measures


class Importance():
    """Centrality."""

    def __init__(self):
        try:
            self.network_name = sys.argv[1]
            self.graph = None
        except IndexError as exc:
            print(f"ERRO {exc}!!"
                  "Digite : \n>python3 sara_centralidade.py <grafo>")
            sys.exit(-1)

    def load_graph(self):
        """carrega um grafo e gera uma lista de vértices."""
        self.graph = nx.read_gml(self.network_name)

    def search(self):
        """realiza pesquisa na rede."""
        graph = centrality_measures.Centrality(self.graph)
        graph.write_seeds()


if __name__ == '__main__':
    importance = Importance()
    importance.load_graph()
    importance.search()
