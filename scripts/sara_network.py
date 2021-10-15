# -*- coding: utf-8 -*-
"""
Script
Generate Networks:
From retweets or mentions(@)

The tweets used to generate these networks are loaded from MongoDB.

SARA
Licença - MIT
LabMIC - UFSJ
2019 - 2021
"""
# system import
from pathlib import Path

# local
from utils import handler_input, is_directed

from sara.core.config import network_path
# intern import
from sara.core.network_generators import (get_mentions_network,
                                          get_retweets_network)
from sara.core.sara_data import SaraData
from sara.core.utils import save_network


def main():
    """Generate networks without weight.

    Generate Graph or Digraph (Directed) from mentions or retweets.
    """

    graph_name, collection, database, directed, limit, source = handler_input()
    directed = is_directed(directed)

    # Create instance used to recovery data from database
    data = SaraData(collection, database)
    if source == 'r':
        # Generate Retweets network
        projection = {'user.screen_name': 1,
                      'retweeted_status.user.screen_name': 1}
        # Recovery tweets
        tweets = data.get_projected_data(projection, limit)
        # Generate network using retweets
        network = get_retweets_network(tweets, directed)

        path_to_save = Path(network_path, "retweets/")
        path_to_save = path_to_save.joinpath(graph_name)
        save_network(network, path_to_save)

    elif source == 'm':
        # Generate mentions network
        projection = {'user.screen_name': 1,
                      'entities.user_mentions.screen_name': 1}
        tweets = data.get_projected_data(projection, limit)
        network = get_mentions_network(tweets, directed)

        # Save to file
        path_to_save = Path(network_path, "mention/")
        path_to_save = path_to_save.joinpath(graph_name)
        save_network(network, path_to_save)
    else:
        raise ValueError("Invalid network type, valid type r or m")


if __name__ == '__main__':
    main()
