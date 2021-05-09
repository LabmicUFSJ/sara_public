"""
Utils
"""
import datetime
import re
from pathlib import Path

import networkx as nx


def max_data_tweets(tweets):
    """Return the date of the most recent tweet."""
    years = []
    for tweet in tweets:
        try:
            # print(tweet.get('id'))
            ano = tweet.get('created_at')
            year = re.sub(r"[+].\d*", " ", ano)
            year = year.replace("  ", "")
            date1 = datetime.datetime.strptime(year, '%a %b %d %H:%M:%S %Y')
            date1 = date1.strftime("%Y-%m-%d")
            years.append(date1)
        except KeyError:
            pass
    return max(years)


def create_path(path):
    """Create a dir."""
    path_tree = Path(path)
    if not path_tree.exists():
        path_tree.mkdir(parents=True, exist_ok=True)
        print(f"Diretório {path_tree} foi criado.")


def save_data(name, data):
    """save data to file json ."""
    with open(name + ".txt", "a") as arq:
        arq.write(str(data))
        arq.write("\n")


def save_network(graph, network_path):
    """Save retweet network to file.

    """
    print(f"Saving network in the path {network_path}")

    network_name = network_path.name
    if not network_path.exists():
        network_path.mkdir(parents=True, exist_ok=True)
    summary_path = network_path.joinpath(f"{network_name}_summary.txt")
    with open(summary_path, "w") as archive:
        archive.write(str(nx.info(graph)))
    print('Saving network with .gml')
    path_network_gml = str(network_path) + f"/{network_name}.gml"
    nx.write_gml(graph, path_network_gml)
    print('Saving network with .gexf')
    nx.write_gml(graph, str(network_path)+f"/{network_name}.gexf")
    graph_ids = nx.convert_node_labels_to_integers(graph)
    # gera traducao de nome para números
    cont = 0
    print('Saving network with .edgelist')
    with open(str(network_path) + f"/traducao_{network_name}", 'a+') as arq:
        for i in graph:
            arq.write(i+":"+str(cont)+"\n")
            cont += 1
    edgelist_name = str(network_path)+f"/{network_name}.edgelist"
    nx.write_edgelist(graph_ids, edgelist_name, data=False)
