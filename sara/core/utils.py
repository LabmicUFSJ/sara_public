"""
Utils
"""
import datetime
import logging
import re
import time
from collections import Counter
from pathlib import Path

import networkx as nx
import requests
from sara.core.exceptions import SaraRequestException

logging.basicConfig(filename='sara.log', level=logging.WARNING)

POLITE_WEB_REQUEST_TIME = 2
WAIT_TIME_RETRY_WEB_REQUEST = 3


def _is_valid(url):
    """Check if url is valid."""
    re_exp = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" +
              "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" +
              "._\\+~#?&//=]*)")
    exp = re.compile(re_exp)
    if exp.match(url):
        return url
    return False


def get_url_from_error(error_msg):
    """Get url from error msg."""

    # search by the match group
    result = re.search('(host=[\'a-z.]*)', error_msg)
    if result:
        # Get first group of match
        group = result.group(0)
        # return url cleaned
        return group.strip("\'host")

    return False


def get_web_url(url, connection_attempt=2):
    """Make polite web request and return a URL.
    In case the fail return the same received URL.
    """
    # polite
    time.sleep(POLITE_WEB_REQUEST_TIME)
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)'
               ' AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/51.0.2704.103 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except (SaraRequestException) as error_msg:
        logging.error('Error to make web request, error %s', error_msg)

        if 'Temporary failure in name resolution' in str(error_msg):
            logging.error('Error name resolution %s', error_msg)
            time.sleep(WAIT_TIME_RETRY_WEB_REQUEST)
            connection_attempt -= 1
            # try a new web request
            if connection_attempt:
                get_web_url(url, connection_attempt)

        # Try extract URL from error message
        url_from_error = get_url_from_error(str(error_msg))
        if _is_valid(url_from_error):
            return url_from_error

    if response.content:
        return response.url

    return url


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
    with open(name + ".txt", "a",  encoding='utf-8') as arq:
        arq.write(str(data))
        arq.write("\n")


def save_network(graph, network_path):
    """Save Graph to file.
    Save graph as GML, gexf and edgelist
    """

    print(f"Saving network in the path {network_path}")
    network_name = network_path.name
    if not network_path.exists():
        network_path.mkdir(parents=True, exist_ok=True)

    # Save network summary
    summary_path = network_path.joinpath(f"{network_name}_summary.txt")
    with open(summary_path, "w", encoding='utf-8') as archive:
        archive.write(str(nx.info(graph)))

    # Save GML
    print('Saving network with .gml')
    path_network_gml = network_path.joinpath(f"{network_name}.gml")
    nx.write_gml(graph, path_network_gml)

    # Sava GEXF
    print('Saving network with .gexf')
    path_gexf = network_path.joinpath(f"{network_name}.gexf")
    nx.write_gml(graph, path_gexf)
    graph_ids = nx.convert_node_labels_to_integers(graph)

    # Save Edgelist
    # gera traducao de nome para números
    print('Saving network with .edgelist')
    path_to_file = network_path.joinpath(f"traducao_{network_name}")
    with open(path_to_file, 'a+', encoding='utf-8') as arq:
        for node, cont in enumerate(graph):
            arq.write(str(node)+":"+str(cont)+"\n")
    edgelist_name = network_path.joinpath(f"{network_name}.edgelist")
    nx.write_edgelist(graph_ids, edgelist_name, data=False)


def load_txt(path_to_file):
    """Load a txt from path and return list.

    Args:
        path_to_file ([type]): [description]
    """
    with open(path_to_file, "r", encoding='utf-8') as lines:
        return [line.strip() for line in lines]


def _extract_hashtag(entities):
    """Extract hashtags."""
    htags = []
    for htag in entities['entities'].get('hashtags'):
        htags.append(htag.get('text'))
    if htags:
        return htags
    return None


def get_hashtags(tweets, k):
    """Return a list of tuples with k most common hashtags.

    The returned tuple is ordered:
    [(a, 10), (b, 5)]
    """
    lista = list(map(_extract_hashtag, tweets))
    # Remove None from list
    listahtags = []
    for htag in filter(None.__ne__, lista):
        listahtags.extend(htag)

    # Most common hashtags
    counter_dict = Counter(listahtags)
    return counter_dict.most_common(k)
