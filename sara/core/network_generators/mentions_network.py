"""
Generate the mentions network.

Source: User mentioned
Destination: The user who made the mention.
Example in a Digraph:
A -> B
The user A was mentioned by user B.
"""
import os
import sys

import pandas as pd
import networkx as nx

from sara.core.config import network_path
from sara.core.utils import create_path

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

def mentions_network(name, tweets, directed):
    """Generate mentions network."""

    if directed:
        print("------\nGerando uma rede: direcionada.")
        # Generate a Digraph
        graph = nx.DiGraph()
    else:
        print("------\nGerando uma rede: não direcionada.")
        # generate a graph
        graph = nx.Graph()
        # carrega os tweets da coleção..
    try:
        if not tweets:
            raise ValueError('The tweets list is empty.')
    except ValueError as error:
        print(f"erro {error}")
        sys.exit(-1)
    count = 0
    for tweet in tweets:
        destiny = None
        count += 1
        try:
            source = tweet['user'].get('screen_name', None)
            mentions = tweet['entities'].get('user_mentions', None)
        except KeyError:
            continue
        # print(mentions)
        for mention in mentions:
            destiny = mention.get('screen_name', None)
            # elimina self loops.
            if destiny == source:
                continue
            if destiny is not None and source is not None:
                graph.add_edge(source, destiny)

    print(f"Com: {count} tweets")
    print("Utilizando: Menções(@)")
    print(f"Nome da Rede: {name}")
    print(f"Sumário da Rede: \n{nx.info(graph)} \n------")

    # try:
    #     archive = open(network_path + "mention_sumario_" + name, "w")
    # except FileNotFoundError:
    #     os.mkdir(network_path)
    #     archive = open(network_path + "mention_sumario_" + name, "w")
    # archive.write(str(nx.info(graph)))
    # archive.close()
    # nx.write_gml(graph, network_path + name + "_mention.gml")
    # print('Saving network with .gexf')
    # nx.write_gexf(graph, network_path + name + ".gexf")
    # graph_ids = nx.convert_node_labels_to_integers(graph)
    # # gera traducao de nome para números
    # count = 0
    # with open(network_path + "mention_traducao_"+name, 'a+') as arq:
    #     for i in graph:
    #         arq.write(i+":"+str(count)+"\n")
    #         count += 1
    # nx.write_edgelist(graph_ids,
    #                   network_path + name + "_mention.edgelist",
    #                   data=False)

    # return graph

def weighted_mentions_network(name, tweets, directed):
    """Generate Weighted mentions network."""
    weighted_edges =  {}
    if directed:
        print("------\nGerando uma rede: direcionada.")
        # Generate a Digraph
        graph = nx.DiGraph()
    else:
        print("------\nGerando uma rede: não direcionada.")
        # generate a graph
        graph = nx.Graph()
        # carrega os tweets da coleção..
    try:
        if not tweets:
            raise ValueError('The tweets list is empty.')
    except ValueError as error:
        print(f"erro {error}")
        sys.exit(-1)
    count = 0
    for tweet in tweets:
        destiny = None
        count += 1
        try:
            source = tweet['user'].get('screen_name', None)
            mentions = tweet['entities'].get('user_mentions', None)
        except KeyError:
            continue
        # print(mentions)
        for mention in mentions:
            destiny = mention.get('screen_name', None)
            # elimina self loops.
            if destiny == source:
                continue
            if destiny is not None and source is not None:
                w = (source, destiny)
                peso = 0
                if w in weighted_edges:
                    peso = weighted_edges[w]
                    peso+=1
                    weighted_edges[w] = peso
                else:
                    weighted_edges[w] = 1

    elements, dicio_pesos = format_weight_edges(weighted_edges)
    table_pesos = pd.DataFrame(dicio_pesos)
    table_pesos.sort_values(by=['peso'], inplace=True, ascending=False)
    table_pesos.to_csv(network_path+'pesos_'+name+'.csv', index=False)
    graph.add_weighted_edges_from(elements)

    print(f"Com: {count} tweets")
    print("Utilizando: Menções(@)")
    print(f"Nome da Rede: {name}")
    print(f"Sumário da Rede: \n{nx.info(graph)} \n------")

    try:
        archive = open(network_path + "mention_sumario_" + name, "w")
    except FileNotFoundError:
        os.mkdir(network_path)
        archive = open(network_path + "mention_sumario_" + name, "w")
    archive.write(str(nx.info(graph)))
    archive.close()
    nx.write_gml(graph, network_path + name + "_weighted.gml")
    print('Saving network with .gexf')
    nx.write_gexf(graph, network_path + name + "_weighted.gexf")
    graph_ids = nx.convert_node_labels_to_integers(graph)
    # gera traducao de nome para números
    count = 0
    with open(network_path + "mention_traducao_"+name, 'a+') as arq:
        for i in graph:
            arq.write(i+":"+str(count)+"\n")
            count += 1
    nx.write_edgelist(graph_ids,
                      network_path + name + "_weighted.edgelist",
                      data=True)

    return graph
