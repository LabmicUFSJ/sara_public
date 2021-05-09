"""
Generate the mentions network.

Source: The user who made the mention.
Destination: User mentionaned;

Example in a Digraph:
A <- B
The user A was mentioned by user B.

"""

from sara.core.network_generators.commons import (format_weighted_edges,
                                                  get_networkx_instance,
                                                  validate_input)


def get_mentions_network(tweets, directed):
    """Generate mentions network.
    Arguments:
        Tweets: List of tweets (dictionary)
        directed : True or False (Boolean)
    Returns:
        An Graph or Digraph from networkx
    """
    graph = get_networkx_instance(directed)
    validate_input(tweets)
    for tweet in tweets:
        destiny = None
        try:
            source = tweet['user'].get('screen_name', None)
            mentions = tweet['entities'].get('user_mentions')
        except KeyError:
            continue
        for mention in mentions:
            destiny = mention.get('screen_name')
            # elimina self loops.
            if destiny == source:
                continue
            if destiny is not None and source is not None:
                graph.add_edge(source, destiny)
    return graph


def get_weighted_mentions_network(tweets, directed):
    """Generate weighted mentions network.
        The weight is generate from the number the mentions.
        Arguments:
            Tweets: List of tweets (dictionary)
            directed : True or False (Boolean)
        Returns:
            An Graph or Digraph from networkx
    """
    weighted_edges = {}
    graph = get_networkx_instance(directed)
    validate_input(tweets)
    for tweet in tweets:
        destiny = None
        try:
            source = tweet['user'].get('screen_name')
            mentions = tweet['entities'].get('user_mentions')
        except KeyError:
            continue
        for mention in mentions:
            destiny = mention.get('screen_name')
            # not allow self loops.
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

    elements = format_weighted_edges(weighted_edges)
    graph.add_weighted_edges_from(elements)
    return graph
