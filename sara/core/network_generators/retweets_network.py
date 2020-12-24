# -*- coding: utf-8 -*-
"""
Gera a rede de Retweets.
Generate the Retweets of Network.
Example in Digraph:
A -> B

The user B was retweeted the user A.
"""
import os
import sys

import pandas as pd
import networkx as nx

from sara.core.config import network_path
from sara.core.utils import create_path

# Check if there is a path and create a dir, if it does not exist.
create_path(network_path)

def format_weight_edges(retweeted):
    elements = []
    elements_dict = []
    for key, value in retweeted.items():
        source, destiny = key
        weight = value
        elements.append((source, destiny, weight))
        elements_dict.append({'origem':source, 'destino':destiny,
                              'peso':weight})
    return elements, elements_dict

def retweets_network(nome_rede, tweets, directed):
    """Generate retweet network."""
    # grafo não direcionado
    if directed:
        print("------\nGerando uma rede direcionada.")
        graph = nx.DiGraph()
    else:
        print("------\nGerando uma rede não direcionada.")
        graph = nx.Graph()
    try:
        # limitando o número de tweets utilizado..
        if not tweets:
            raise ValueError('The tweet list is empty.')
    except ValueError as error:
        print(f"erro {error}")
        sys.exit(-1)
    cont = 0
    for tweet in tweets:
        destino = None
        try:
            cont += 1
            origem = tweet['user']['screen_name']
        except KeyError:
            pass
        try:
            destino = tweet['retweeted_status']['user']['screen_name']
        except KeyError:
            origem = None
        # elimina self loops.
        if destino == origem:
            continue
        if destino is not None and origem is not None:
            graph.add_edge(origem, destino)

    print(f"Number Tweets: {cont} ")
    print("Network Type: Retweets")
    print(f"Network Name: {nome_rede}")
    print(f"Sumário da Rede: \n{nx.info(graph)} \n------")
    # try:
    #     arquivo = open(network_path + "sumario_" + nome_rede, "w")
    # except FileNotFoundError:
    #     os.mkdir(network_path)
    #     arquivo = open(network_path + "sumario_" + nome_rede, "w")
    # arquivo.write(str(nx.info(graph)))
    # arquivo.close()
    # print('Saving network with .gml')
    # nx.write_gml(graph, network_path + nome_rede + ".gml")
    # print('Saving network with .gexf')
    # nx.write_gexf(graph, network_path + nome_rede + ".gexf")
    # graph_ids = nx.convert_node_labels_to_integers(graph)
    # # gera traducao de nome para números
    # cont = 0
    # with open(network_path + "traducao_"+nome_rede, 'a+') as arq:
    #     for i in graph:
    #         arq.write(i+":"+str(cont)+"\n")
    #         cont += 1
    # nx.write_edgelist(graph_ids,
    #                   network_path + nome_rede + ".edgelist", data=False)
    # return graph

def weigth_retweet_network(nome_rede, tweets, directed):
    """Generate Weighted retweet network."""
    retweet_edges = {}
    # grafo não direcionado
    if directed:
        print("------\nGerando uma rede direcionada.")
        graph = nx.DiGraph()
    else:
        print("------\nGerando uma rede não direcionada.")
        graph = nx.Graph()
    try:
        # limitando o número de tweets utilizado..
        if not tweets:
            raise ValueError('The tweet list is empty.')
    except ValueError as error:
        print(f"erro {error}")
        sys.exit(-1)
    cont = 0
    for tweet in tweets:
        destino = None
        try:
            cont += 1
            origem = tweet['user']['screen_name']
        except KeyError:
            pass
        try:
            destino = tweet['retweeted_status']['user']['screen_name']
        except KeyError:
            origem = None
        # elimina self loops.
        if destino == origem:
            continue
        if destino is not None and origem is not None:
            w = (origem, destino)
            peso = 0
            if w in retweet_edges:
                peso = retweet_edges[w]
                peso+=1
                retweet_edges[w] = peso
            else:
                retweet_edges[w] = 1

    elements, dicio_pesos = format_weight_edges(retweet_edges)
    table_pesos = pd.DataFrame(dicio_pesos)
    table_pesos.sort_values(by=['peso'], inplace=True, ascending=False)
    table_pesos.to_csv(network_path+'pesos_'+nome_rede+'.csv', index=False)
    graph.add_weighted_edges_from(elements)


    print(f"Number Tweets: {cont} ")
    print("Network Type: Retweets")
    print(f"Network Name: {nome_rede}")
    print(f"Sumário da Rede: \n{nx.info(graph)} \n------")
    try:
        arquivo = open(network_path + "sumario_" + nome_rede, "w")
    except FileNotFoundError:
        os.mkdir(network_path)
        arquivo = open(network_path + "sumario_" + nome_rede, "w")
    arquivo.write(str(nx.info(graph)))
    arquivo.close()
    print('Saving network with .gml')
    nx.write_gml(graph, network_path + nome_rede + "_weighted.gml")
    print('Saving network with .gexf')
    nx.write_gexf(graph, network_path + nome_rede + "_weighted.gexf")
    graph_ids = nx.convert_node_labels_to_integers(graph)
    # gera traducao de nome para números
    cont = 0
    with open(network_path + "traducao_"+nome_rede, 'a+') as arq:
        for i in graph:
            arq.write(i+":"+str(cont)+"\n")
            cont += 1
    nx.write_edgelist(graph_ids,
                      network_path + nome_rede + "_weighted.edgelist",
                      data=True)
    return graph

