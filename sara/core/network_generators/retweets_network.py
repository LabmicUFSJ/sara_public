# -*- coding: utf-8 -*-
"""
Gera a rede de Retweets.
Generate the Retweets of Network.
Example in Digraph:
A -> B

The user B was retweeted the user A.
"""
from sara.core.network_generators.commons import (format_weighted_edges,
                                                  get_networkx_instance)


def get_retweets_network(tweets, directed):
    """Generate retweet network.

    Return an nx.Digraph network or Nx.Graph() network
    """
    graph = get_networkx_instance(directed)
    for tweet in tweets:
        destiny = None
        try:
            source = tweet['user']['screen_name']
        except KeyError:
            pass
        try:
            destiny = tweet['retweeted_status']['user']['screen_name']
        except KeyError:
            source = None
        # Not allow self loops
        if destiny == source:
            continue
        if destiny is not None and source is not None:
            graph.add_edge(source, destiny)

    return graph


def get_weigthed_retweet_network(tweets, directed):
    """Generate Weighted retweet network."""
    retweet_edges = {}
    if not tweets:
        ValueError("The tweet list is empty.")

    graph = get_networkx_instance(directed)

    for tweet in tweets:
        destiny = None
        try:
            source = tweet['user']['screen_name']
        except KeyError:
            pass
        try:
            destiny = tweet['retweeted_status']['user']['screen_name']
        except KeyError:
            source = None
        # elimina self loops.
        if destiny == source:
            continue
        if destiny is not None and source is not None:
            path_edge = (source, destiny)
            weight = 0
            if path_edge in retweet_edges:
                weight = retweet_edges[path_edge]
                weight += 1
                retweet_edges[path_edge] = weight
            else:
                retweet_edges[path_edge] = 1

    elements = format_weighted_edges(retweet_edges)
    graph.add_weighted_edges_from(elements)
    return graph
