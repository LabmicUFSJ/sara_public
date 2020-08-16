"""
Generate the mentions network.

Source: User mentioned
Destination: The user who made the mention.
Example in a Digraph:
A -> B
The user A was mentioned by user B.
"""
import sys
import os

import networkx as nx

from sara.core.database import inicia_conexao, _load_database
from sara.core.config import network_path
from sara.core.utils import create_path


create_path(network_path)


def mentions_network(name, database, collection, graph_type, limit_tweets):
    """Generate mentions network."""

    cliente = inicia_conexao()
    colecao = _load_database(cliente, database, collection)

    if "True" in graph_type:
        print("------\nGerando uma rede: direcionada.")
        # Generate a Digraph
        graph = nx.DiGraph()
    else:
        print("------\nGerando uma rede: não direcionada.")
        # generate a graph
        graph = nx.Graph()
        # carrega os tweets da coleção..
    try:
        # limitando o número de tweets utilizado..
        tweets = colecao.find().limit(limit_tweets)
    except Exception as e:
        print(f"erro {e}")
        sys.exit(-1)
    count = 0
    for tweet in tweets:
        destiny = None
        count += 1
        destiny = tweet['user'].get('screen_name', None)
        mentions = tweet['entities'].get('user_mentions', None)
        # print(mentions)
        for mention in mentions:
            source = mention.get('screen_name', None)
            if destiny is not None and source is not None:
                graph.add_edge(source, destiny)

    print(f"Com: {count} tweets")
    print("Utilizando: Menções(@)")
    print(f"Nome da Rede: {name}")
    print(f"Originada da Colecao: {collection}\n--------")
    print(f"Sumário da Rede: \n{nx.info(graph)} \n------")
    try:
        archive = open(network_path + "mention_sumario_" + name, "w")
    except FileNotFoundError:
        os.mkdir(network_path)
        archive = open(network_path + "mention_sumario_" + name, "w")
    archive.write(str(nx.info(graph)))
    archive.close()
    nx.write_gml(graph, network_path + name + "_mention.gml")
    graph_ids = nx.convert_node_labels_to_integers(graph)
    # gera traducao de nome para números
    count = 0
    with open(network_path + "mention_traducao_"+name, 'a+') as arq:
        for i in graph:
            arq.write(i+":"+str(count)+"\n")
            count += 1
    nx.write_edgelist(graph_ids,
                      network_path + name + "_mention.edgelist",
                      data=False)

    # nx.write_gexf(graph,"retweets2.gexf")
