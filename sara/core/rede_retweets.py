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

import networkx as nx

import sara.core.database as bd
from sara.core.config import network_path
from sara.core.utils import create_path


# Check if there is a path and create a dir, if it does not exist.
create_path(network_path)


def main(nome_rede, nome_base, nome_colecao, direcionada, limite_tweets):
    cliente = bd.inicia_conexao()
    colecao = bd.carregar_banco(cliente, nome_base, nome_colecao)
    # grafo não direcionado
    if "True" in direcionada:
        print("------\nGerando uma rede direcionada.")
        grafo = nx.DiGraph()
    else:
        print("------\nGerando uma rede não direcionada.")
        grafo = nx.Graph()

    # carrega os tweets da coleção..
    try:
        # limitando o número de tweets utilizado..
        tweets = colecao.find().limit(limite_tweets)
    except Exception as e:
        print(f"erro {e}")
        sys.exit()
    cont = 0
    for tweet in tweets:
        destino = None
        try:
            cont += 1
            destino = tweet['user']['screen_name']
        except Exception:
            pass
        try:
            origem = tweet['retweeted_status']['user']['screen_name']
        except Exception:
            origem = None
        if destino is not None and origem is not None:
            grafo.add_edge(origem, destino)

    print(f"Com: {cont} tweets")
    print("Utilizando: Retweets")
    print(f"Nome da Rede: {nome_rede}")
    print(f"Originada da Colecao: {nome_colecao}\n--------")
    print(f"Sumário da Rede: \n{nx.info(grafo)} \n------")
    try:
        arquivo = open(network_path + "sumario_" + nome_rede, "w")
    except FileNotFoundError:
        os.mkdir(network_path)
        arquivo = open(network_path + "sumario_" + nome_rede, "w")
    arquivo.write(str(nx.info(grafo)))
    arquivo.close()
    nx.write_gml(grafo, network_path + nome_rede + ".gml")
    grafo_ids = nx.convert_node_labels_to_integers(grafo)
    # gera traducao de nome para números
    cont = 0
    with open(network_path + "traducao_"+nome_rede, 'a+') as arq:
        for i in grafo:
            arq.write(i+":"+str(cont)+"\n")
            cont += 1
    nx.write_edgelist(grafo_ids,
                      network_path + nome_rede + ".edgelist", data=False)
    # nx.write_gexf(grafo,"retweets2.gexf")
