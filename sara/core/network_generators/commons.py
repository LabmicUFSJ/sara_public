"""Comnons network utils."""
import sys

import networkx as nx


def validate_input(tweets):
    """Validate the tweets inputed."""
    try:
        if not tweets:
            raise ValueError('The tweets list is empty.')
    except ValueError as error:
        print(f"erro {error}")
        sys.exit(-1)


def format_weighted_edges(retweeted):
    """Return a dictionary with the weight."""
    elements = []
    for key, value in retweeted.items():
        source, destiny = key
        weight = value
        elements.append((source, destiny, weight))
    return elements


def show_info(network_name, count, graph):
    """Show information about the network."""
    print(f"Number Tweets: {count} ")
    print("Network Type: Retweets")
    print(f"Network Name: {network_name}")
    print(f"Summary: \n{nx.info(graph)} \n------")


def get_networkx_instance(directed):
    """Return a nx.Digraph() or nx.Graph() instance.
    Argument: directed True -> Return nx.Digraph()
        directed False - > Return nx.Graph()
    """
    if directed:
        return nx.DiGraph()
    return nx.Graph()