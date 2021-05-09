# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central Estrutural -
Generate Networks:
From retweets or mentions(@)

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
"""
# system import
from pathlib import Path

from sara.core.config import network_path
# intern import
from sara.core.network_generators import (get_mentions_network,
                                          get_retweets_network)
from sara.core.sara_data import SaraData
from sara.core.utils import save_network


def main(network_name, collection_name, directed, limit, source):
    """Inicia a geração da rede."""
    print("---Inputed Data---\n")
    print(f"Network name: {network_name} \n"
          f"Collection: {collection_name} \n"
          f"Directed: {directed} \n"
          f"Type: {source}")
    print("-----------------")
    if 'True' in directed:
        directed = True
    elif 'False' in directed:
        directed = False
    else:
        raise ValueError("Error, Valid type is True or False."
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
