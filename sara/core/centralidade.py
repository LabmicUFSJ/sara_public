# -*- coding: utf-8 -*-
import csv

import networkx as nx

import sara.core.database as bd
from sara.core.config import centrality_path
from sara.core.utils import check_path

"""
Realiza o cálculo das centralidades
Centrality
* Calcula retweets, degree, pagerank, betweenness, curtidas
"""


# Check if a path exists, and create a dir if not exist.
check_path(centrality_path)


def top(lista, numero):
    """exibe o top numero de elementos."""
    cont = 1
    for i in lista:
        print(i)
        if cont == numero:
            break
        cont += 1


def key_retweets_dic(item):
    "key de retweets"
    return item[1]


def key_curtidas_dic(item):
    """Retorna a key de curtida"""
    return item[2]


def prepara_tweets(tweets):
    """adiciona os tweets em uma lista."""
    l_tweets = []
    for cursor in tweets:
        for i in cursor:
            l_tweets.append(i)
    return l_tweets


def get_key(item):
    """retorna uma chave de um item."""
    return item[1]


def analise_betweenness(grafo):
    """realiza analise de betweenness_centrality"""

    rede = nx.betweenness_centrality(grafo)
    lista_bet = []
    for j in rede:
        # print(j,rede[j])
        lista_bet.append([j, rede[j]])
    lista_bet = sorted(lista_bet, key=get_key, reverse=True)
    return lista_bet


def consulta_origem(user, tweets):
    """consulta o nó de origem"""
    for i in tweets:
        try:
            # print(i)
            # print(i['retweet_count'],i['favorite_count'],i['user']['screen_name'])
            # exit()
            numero_retweets = i['retweet_count']
            numero_curtidas = i['favorite_count']
            nome = i['user']['screen_name']
            if nome not in user:
                user[nome] = [int(numero_retweets), int(numero_curtidas)]
            else:
                antigo = user[nome]
                user[nome] = [
                    (antigo[0] + int(numero_retweets)) / 2,
                    (antigo[1] + int(numero_curtidas)) / 2,
                ]
        except Exception:
            pass
    return user


def consulta(user, tweets):
    """Consulta de tweets"""
    for i in tweets:
        try:
            numero_retweets = i['retweeted_status']['retweet_count']
            numero_curtidas = i['retweeted_status']['favorite_count']
            nome = i['retweeted_status']['user']['screen_name']
            if nome not in user:
                user[nome] = [int(numero_retweets), int(numero_curtidas)]
            else:
                antigo = user[nome]
                user[nome] = [
                    (antigo[0] + int(numero_retweets)) / 2,
                    (antigo[1] + int(numero_curtidas)) / 2,
                ]
        except Exception:
            # print(e)
            pass
    return user


def carrega_grafo(nome_rede):
    """Carrega o grafo .gml"""
    grafo = nx.read_gml(nome_rede + ".gml")
    return grafo


def pagerank(grafo):
    """Centralidade por pagerank"""
    rank = nx.pagerank(grafo)
    lista_pagerank = []
    for j in rank:
        # print(j,rede[j])
        lista_pagerank.append([j, rank[j]])
    lista_pagerank = sorted(lista_pagerank, key=get_key, reverse=True)
    return lista_pagerank


def degree(grafo):
    """Cenralidade por grau"""
    degree = nx.degree_centrality(grafo)
    lista_degree = []
    for j in degree:
        # print(j,rede[j])
        lista_degree.append([j, degree[j]])
    lista_degree = sorted(lista_degree, key=get_key, reverse=True)
    return lista_degree


def salvar_csv(nome_rede, lista_betweenness, lista_retweets, lista_curtidas,
               lista_degree,
               lista_pagerank):
    """Salva um csv"""

    csvfile = open(centrality_path + "lista_relacao_" + nome_rede + ".csv",
                   "w", newline='')
    nome_campos = ['Degree', 'Betweenness', 'Retweets', 'Curtidas', 'PageRank']
    writer = csv.DictWriter(csvfile, fieldnames=nome_campos)
    writer.writeheader()
    for i in range(0, len(lista_betweenness)):
        writer.writerow(
            {
                'Degree': lista_degree[i][1],
                'Betweenness': lista_betweenness[i][1],
                'Retweets': lista_retweets[i],
                'Curtidas': lista_curtidas[i],
                'PageRank': lista_pagerank[i][1],
            }
        )

    csvfile.close()


def imprimir_sementes(sementes, nome_metodo, nome_rede):
    """Imprir sementes"""
    arq_sementes = open(centrality_path + 
                        "sementes_" + nome_metodo + "_" + nome_rede, "w")
    for i in sementes:
        arq_sementes.write(str(i[0]) + "\n")
    arq_sementes.close()


def main(nome_base, colecao, lista_nos, nome_rede):
    cliente = bd.inicia_conexao()
    colecao = bd.carregar_banco(cliente, nome_base, colecao)

    # inica a conexao com twitter
    # api = conexao.inicia_conexao()

    # utilizado para selecionar o titulo contendo
    # a palavra senado maiusculo e minúsculo.
    # retorno=colecao.find({"titulo":{"$regex":"senado","$options":"i"}})
    # for i in retorno:
    #     print(i)
    # print("Dados",nome_base,nome_colecao,lista_nos,nome_rede)
    tweets = []
    for nome_no in lista_nos:
        tweets.append(
            colecao.find(
                {"user.screen_name": {"$regex": nome_no, "$options": "i"}}
            )
        )

    user = {}
    tweets = prepara_tweets(tweets)
    user = consulta_origem(user, tweets)
    print(user)

    user = consulta(user, tweets)
    print("pos", user)

    lista = []
    for i in user:
        # Nome, Retweets, Curtidas
        lista.append([i, user[i][0], user[i][1]])
    print("Retweets")
    arq_retweets = open(centrality_path + "sementes_retweets_" + nome_rede, "w")
    retorno = sorted(lista, key=key_retweets_dic, reverse=True)
    # print(retorno)
    # print("LN",lista_nos)
    lista_retweets = []
    lista_curtidas = []
    lista_betweenness = []
    lista_degree = []
    lista_pagerank = []
    grafo = carrega_grafo(nome_rede)
    lista_pagerank = pagerank(grafo)
    imprimir_sementes(lista_pagerank, "pagerank", nome_rede)
    lista_betweenness = analise_betweenness(grafo)
    imprimir_sementes(lista_betweenness, "Betweenness", nome_rede)
    lista_degree = degree(grafo)
    imprimir_sementes(lista_degree, "Degree", nome_rede)
    for retweets in retorno:
        for no in lista_nos:
            if retweets[0].lower() == no.lower():
                lista_retweets.append(retweets[1])
                arq_retweets.write(str(no) + "\n")
    arq_retweets.close()
    arq_curtidas = open(centrality_path + "sementes_curtidas_" + nome_rede, "w")
    print("Curtidas")
    for curtidas in sorted(lista, key=key_curtidas_dic, reverse=True):
        for no in lista_nos:
            if curtidas[0].lower() == no.lower():
                lista_curtidas.append(float(curtidas[2]))
                arq_curtidas.write(str(no) + "\n")
    print(len(lista_curtidas), len(lista_retweets), len(lista_betweenness),
          len(lista_degree),
          len(lista_degree))

    salvar_csv(
        nome_rede,
        lista_betweenness,
        lista_retweets,
        lista_curtidas,
        lista_degree,
        lista_pagerank,
    )
    arq_curtidas.close()
