# -*- coding: utf-8 -*-
"""
Script
Generate Networks with weights:
From retweets or mentions(@)

SARA
Licença - MIT
LabMIC - UFSJ
2019 - 2021
"""
# system import
from pathlib import Path

from sara.core.config import network_path
# intern import
from sara.core.network_generators import (get_weighted_mentions_network,
                                          get_weigthed_retweet_network)
from sara.core.sara_data import SaraData
from sara.core.utils import save_network

# local
from utils import handler_input, is_directed


def main():
    """Generate weighted graph."""

    # Get user input
    graph_name, collection, database, directed, limit, source = handler_input()
    directed = is_directed(directed)

    data = SaraData(collection, database)
    if source == 'r':
        # Generate Retweets network
        projection = {'user.screen_name': 1,
                      'retweeted_status.user.screen_name': 1}
        tweets = data.get_projected_data(projection, limit)

        network = get_weigthed_retweet_network(tweets, directed)

        path_to_save = Path(network_path, "retweets_with_weight/")
        path_to_save = path_to_save.joinpath(graph_name)
        save_network(network, path_to_save)
    elif source == 'm':
        # Generate mentions network
        projection = {'user.screen_name': 1,
                      'entities.user_mentions.screen_name': 1}
        tweets = data.get_projected_data(projection, limit)

        network = get_weighted_mentions_network(tweets, directed)

        path_to_save = Path(network_path, "mention_with_weight/")
        path_to_save = path_to_save.joinpath(graph_name)
        save_network(network, path_to_save)
    else:
        raise ValueError("Invalid network type, valid type r or m")


if __name__ == '__main__':
    main()
