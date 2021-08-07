# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central Estrutural -
Generate Networks with weights:
From retweets or mentions(@)

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
"""
# system import
import sys
from pathlib import Path

from sara.core.config import network_path
# intern import
from sara.core.network_generators import (get_weighted_mentions_network,
                                          get_weigthed_retweet_network)
from sara.core.sara_data import SaraData
from sara.core.utils import save_network


def main():
    """Inicia a geração da rede."""
    try:
        network_name = sys.argv[1]
        collection_name = sys.argv[2]
        directed = sys.argv[3]
        limit = int(sys.argv[4])
        source = sys.argv[5]
        # limite de tweets a serem utilizados
    except IndexError as exc:
        print(f"erro {exc}")
        print(f"ERRO!!\nDigite:\n>python3 {sys.argv[0]} <nome_rede>"
              " <nome_colecao> <True||False> <limite> <r|m>")
        print("Info True: Rede direcionada, False: Rede não direcionada"
              "\nInfo limite:0 para utilizar a base completa")
        print("Info r: para gerar uma rede utilizando retweets, "
              "m: gera a rede utilizando menções(@)")
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
            network = get_weigthed_retweet_network(tweets, directed)
            path_to_save = Path(network_path, "retweets_with_weight/")
            path_to_save = path_to_save.joinpath(network_name)
            save_network(network, path_to_save)
        elif source == 'm':
            # Generate mentions network
            projection = {'user.screen_name': 1,
                          'entities.user_mentions.screen_name': 1}
            tweets = data.get_projected_data(projection, limit)
            network = get_weighted_mentions_network(tweets, directed)
            path_to_save = Path(network_path, "mention_with_weight/")
            path_to_save = path_to_save.joinpath(network_name)
            save_network(network, path_to_save)
        else:
            raise ValueError("Invalid network type, valid type r or m")

    except (IndexError, ValueError) as error:
        print(f"Error {error}")


if __name__ == '__main__':
    main()
