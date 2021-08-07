# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Generate Networks:
From retweets or mentions(@)

The tweets used to generate these networks are loaded from MongoDB.

SARA
Licença - MIT
LabMIC - UFSJ
2019 - 2021
Carlos Barbosa
"""
# system import
import sys
from pathlib import Path

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
    try:
        network_name = sys.argv[1]
        collection_name = sys.argv[2]
        directed = sys.argv[3]
        limit = int(sys.argv[4])
        source = sys.argv[5]
    except IndexError as exc:
        print(f"Erro: {exc}")
        print(f"ERRO!!\nInput:\n>python {sys.argv[0]} <network_name>"
              " <collection_name> <True||False> <limit_of_tweets> <r|m>")
        print("Info True: Directed network, False: Undirected network"
              "\nInfo number_of_tweets: 0 use all tweets stored in "
              "collection.")
        print("Info r: generate retweet network, "
              "m: generate mention(@) network")
        sys.exit(-1)

    print("---Inputed Data---\n")
    print(f"Network name: {network_name} \n"
          f"Collection: {collection_name} \n"
          f"Directed: {directed} \n"
          f"Type: {source}")
    print("-----------------")
    if directed.lower() == 'true':
        directed = True
    elif directed.lower() == 'false':
        directed = False
    else:
        raise TypeError("Error, Valid type is True or False."
                        f"You passed the type: {type(directed)}")
    try:
        data = SaraData(collection_name, storage_type='mongodb')
        if source == 'r':
            # Generate Retweets network
            projection = {'user.screen_name': 1,
                          'retweeted_status.user.screen_name': 1}
            tweets = data.get_projected_data(projection, limit)
            network = get_retweets_network(tweets, directed)
            path_to_save = Path(network_path, "retweets/")
            path_to_save = path_to_save.joinpath(network_name)
            save_network(network, path_to_save)
        elif source == 'm':
            # Generate mentions network
            projection = {'user.screen_name': 1,
                          'entities.user_mentions.screen_name': 1}
            tweets = data.get_projected_data(projection, limit)
            network = get_mentions_network(tweets, directed)
            path_to_save = Path(network_path, "mention/")
            path_to_save = path_to_save.joinpath(network_name)
            save_network(network, path_to_save)
        else:
            raise ValueError("Invalid network type, valid type r or m")

    except (IndexError, ValueError) as error:
        print(f"Error {error}")


if __name__ == '__main__':
    main()
