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
from sara.core.rede_retweets import main as retweet_network
from sara.core.rede_mencoes import mentions_network


def main():
    """Inicia a geração da rede."""
    try:
        network_name = sys.argv[1]
        database_name = sys.argv[2]
        collection_name = sys.argv[3]
        directed = sys.argv[4]
        limit = int(sys.argv[5])
        source = sys.argv[6]
        # limite de tweets a serem utilizados
    except IndexError as exc:
        print(f"erro {exc}")
        print(f"ERRO!!\nDigite:\n>python3 {sys.argv[0]} <nome_rede>"
              " <nome_base> <nome_colecao> <True||False> <limite> <r|m>")
        print("Info True: Rede direcionada, False: Rede não direcionada"
              "\nInfo limite:0 para utilizar a base completa")
        print("Info r: para gerar uma rede utilizando retweets, "
              "m: gera a rede utilizando menções(@)")
        sys.exit()

    try:
        if source == 'r':
            # Generate Retweets network
            retweet_network(network_name, database_name, collection_name,
                            directed, limit)
        elif source == 'm':
            # Generate mentions network
            mentions_network(network_name, database_name, collection_name,
                             directed, limit)
        else:
            raise IndexError

    except IndexError:
        print("Escolha o modo de geração da rede r - retweets ou m- mentions")


if __name__ == '__main__':
    main()
