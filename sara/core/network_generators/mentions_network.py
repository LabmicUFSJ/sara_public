"""
Generate the mentions network.

Source: User mentioned
Destination: The user who made the mention.
Example in a Digraph:
A -> B
The user A was mentioned by user B.
"""
import sys

import networkx as nx
import pandas as pd
from sara.core.config import network_path
from sara.core.utils import create_path

create_path(network_path)


def _format_weight_edges(retweeted):
    """Format weight edges."""
    elements = []
    elements_dict = []
    for key, value in retweeted.items():
        source, destiny = key
        weight = value
        elements.append((source, destiny, weight))
        elements_dict.append({'origem': source, 'destino': destiny,
                              'peso': weight})
    return elements, elements_dict


def _show_stats(graph, tweets, name):
    """Show stats about the network."""
    print(f"Com: {len(tweets)} tweets")
    print("Utilizando: Menções(@)")
    print(f"Nome da Rede: {name}")
    print(f"Sumário da Rede: \n{nx.info(graph)} \n------")


def _validade_input(tweets):
    """Valided tweet input."""
    try:
        if not tweets:
            raise ValueError('The tweets list is empty.')
    except ValueError as error:
        print(f"erro {error}")
        sys.exit(-1)


def _get_network(directed):
    """Return a nx.Digraph() or nx.Graph() instance.
    Argument: directed True -> Return nx.Digraph()
        directed False - > Return nx.Graph()
    """
    if directed:
        print("------\nGerando uma rede: direcionada.")
        return nx.DiGraph()
    print("------\nGerando uma rede: não direcionada.")
    return nx.Graph


def mentions_network(name, tweets, directed):
    """Generate mentions network."""
    graph = _get_network(directed)
    _validade_input(tweets)
    for tweet in tweets:
        destiny = None
        try:
            source = tweet['user'].get('screen_name', None)
            mentions = tweet['entities'].get('user_mentions', None)
        except KeyError:
            continue
        for mention in mentions:
            destiny = mention.get('screen_name', None)
            # elimina self loops.
            if destiny == source:
                continue
            if destiny is not None and source is not None:
                graph.add_edge(source, destiny)

    _show_stats(graph, tweets, name)
    return graph


def weighted_mentions_network(name, tweets, directed):
    """Generate Weighted mentions network."""
    weighted_edges = {}
    graph = _get_network(directed)
    _validade_input(tweets)
    for tweet in tweets:
        destiny = None
        try:
            source = tweet['user'].get('screen_name', None)
            mentions = tweet['entities'].get('user_mentions', None)
        except KeyError:
            continue
        for mention in mentions:
            destiny = mention.get('screen_name', None)
            # elimina self loops.
            if destiny == source:
                continue
            if destiny is not None and source is not None:
                weighted_tuple = (source, destiny)
                weight = 0
                if weighted_tuple in weighted_edges:
                    weight = weighted_edges[weighted_tuple]
                    weight += 1
                    weighted_edges[weighted_tuple] = weight
                else:
                    weighted_edges[weighted_tuple] = 1

    elements, dict_weights = _format_weight_edges(weighted_edges)
    # save table with weights
    table_weight = pd.DataFrame(dict_weights)
    table_weight.sort_values(by=['weight'], inplace=True, ascending=False)
    table_weight.to_csv(network_path+'weights_'+name+'.csv', index=False)

    graph.add_weighted_edges_from(elements)

    _show_stats(graph, tweets, name)
    return graph
