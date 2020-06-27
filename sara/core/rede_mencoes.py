"""
Generate the mentions network.

Source: User mentioned
Destination: The user who made the mention.
Example in a Digraph:
A -> B
The user A was mentioned by user B.
"""
import os

import networkx as nx

from sara.core.database import carrega_tweets
from sara.core.config import network_path
from sara.core.utils import create_path


create_path(network_path)


def mentions_network(nome_rede, database, collection, graph_type, limit=None):
    """Generate mentions network."""

    if "True" in graph_type:
        print("------\nGerando uma rede: direcionada.")
        # Generate a Digraph
        graph = nx.DiGraph()
    else:
        print("------\nGerando uma rede: não direcionada.")
        # generate a graph
        graph = nx.Graph()

    tweets = carrega_tweets(database, collection, limit)
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
    print(f"Nome da Rede: {nome_rede}")
    print(f"Originada da Colecao: {collection}\n--------")
    print(f"Sumário da Rede: \n{nx.info(graph)} \n------")
    try:
        archive = open(network_path + "mention_sumario_" + nome_rede, "w")
    except FileNotFoundError:
        os.mkdir(network_path)
        archive = open(network_path + "mention_sumario_" + nome_rede, "w")
    archive.write(str(nx.info(graph)))
    archive.close()
    nx.write_gml(graph, network_path + nome_rede + "_mention.gml")
    graph_ids = nx.convert_node_labels_to_integers(graph)
    # gera traducao de nome para números
    count = 0
    with open(network_path + "mention_traducao_"+nome_rede, 'a+') as arq:
        for i in graph:
            arq.write(i+":"+str(count)+"\n")
            count += 1
    nx.write_edgelist(graph_ids,
                      network_path + nome_rede + "_mention.edgelist",
                      data=False)

    # nx.write_gexf(graph,"retweets2.gexf")