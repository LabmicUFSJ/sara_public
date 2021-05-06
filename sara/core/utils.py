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
    arq = open(name + ".txt", "a")
    arq.write(str(data))
    arq.write("\n")
    arq.close()


def save_mention_network(graph, network_path):
    """Save mention network to file."""
    try:
        archive = open(network_path + "mention_summary_", "w")
    except FileNotFoundError:
        path_to_save = Path(network_path)
        path_to_save.mkdir(parents=True, exist_ok=True)
        archive = open(network_path + "mention_summary_", "w")
    archive.write(str(nx.info(graph)))
    archive.close()
    nx.write_gml(graph, network_path + ".gml")
    print('Saving network with .gexf')
    nx.write_gexf(graph, network_path + ".gexf")
    graph_ids = nx.convert_node_labels_to_integers(graph)
    # gera traducao de nome para números
    count = 0
    with open(network_path + "mention_traducao_", 'a+') as arq:
        for i in graph:
            arq.write(i+":"+str(count)+"\n")
            count += 1
    nx.write_edgelist(graph_ids, network_path + ".edgelist", data=True)


def save_retweet_network(graph, network_path):
    """Save retweet network to file."""
    try:
        archive = open(network_path + "summary_", "w")
    except FileNotFoundError:
        path_to_save = Path(network_path)
        path_to_save.mkdir(parents=True, exist_ok=True)
        archive = open(network_path + "summary_", "w")
    archive.write(str(nx.info(graph)))
    archive.close()
    print('Saving network with .gml')
    nx.write_gml(graph, network_path+".gml")
    print('Saving network with .gexf')
    nx.write_gexf(graph, network_path + ".gexf")
    graph_ids = nx.convert_node_labels_to_integers(graph)
    # gera traducao de nome para números
    cont = 0
    with open(network_path + "traducao_", 'a+') as arq:
        for i in graph:
            arq.write(i+":"+str(cont)+"\n")
            cont += 1
    nx.write_edgelist(graph_ids, network_path + ".edgelist", data=False)
