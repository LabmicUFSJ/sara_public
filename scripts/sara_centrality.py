# -*- coding: utf-8 -*-
"""
Script to make centrality analysis

This script uses the Sara Framework.

SARA
Licença - MIT
LabMIC - UFSJ
2019 - 2021
"""
import sys

from sara.core.sara_graph import load_graph
from sara.core.centrality import Centrality


class Importance():
    """Centrality."""

    def __init__(self):
        try:
            self.network_name = sys.argv[1]
            self.graph = None
        except IndexError as exc:
            print(f"ERRO {exc}!!"
                  "Input : \n>python {sys.argv[0]} <network.gml>")
            sys.exit(-1)

    def load_graph(self):
        """Load a graph."""
        self.graph = load_graph(self.network_name)

    def save_ranking(self):
        """Make centrality analysis and save a rank nodes.
        """
        graph = Centrality(self.graph)
        graph.write_seeds()


if __name__ == '__main__':
    importance = Importance()
    importance.load_graph()
    importance.save_ranking()
