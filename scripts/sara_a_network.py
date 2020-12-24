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
import sys

# intern import
from sara.core.network_generators.retweets_network import retweets_network
from sara.core.network_generators.mentions_network import mentions_network
from sara.core.sara_data import SaraData

def main():
    """Inicia a geração da rede."""
    try:
        network_name = sys.argv[1]
        # collection_name = sys.argv[2]
        directed = sys.argv[2]
        limit = int(sys.argv[3])
        source = sys.argv[4]
        # limite de tweets a serem utilizados
    except IndexError as exc:
        print(f"erro {exc}")
        print(f"ERRO!!\nDigite:\n>python3 {sys.argv[0]} <nome_rede>"
              " <True||False> <limite> <r|m>")
        print("Info True: Rede direcionada, False: Rede não direcionada"
              "\nInfo limite:0 para utilizar a base completa")
        print("Info r: para gerar uma rede utilizando retweets, "
              "m: gera a rede utilizando menções(@)")
        sys.exit()
    collections = SaraData("", storage_type='mongodb').get_all_collections()
    try:
        tweets_collection = []
        for coll in collections:
            print(f'Collection {coll}')
            data = SaraData(coll, storage_type='mongodb')
            if source == 'r':
                print('retweet')
                # Generate Retweets network
                projection = {'user.screen_name':1,
                            'retweeted_status.user.screen_name':1}
                tweets = data.get_projected_data(projection, limit)
                tweets_collection.extend(tweets)
            elif source == 'm':
                print('mention')
                # Generate mentions network
                projection = {'user.screen_name':1,
                            'entities.user_mentions.screen_name':1}
                tweets = data.get_projected_data(projection, limit)
                tweets_collection.extend(tweets)
            else:
                raise IndexError
        print(len(tweets_collection))
        if source == 'r':
            retweets_network(network_name, tweets_collection, directed)
        elif source =='m':
            mentions_network(network_name, tweets_collection, directed)
    except IndexError:
        print("Escolha o modo de geração da rede r - retweets ou m- mentions")


if __name__ == '__main__':
    main()
