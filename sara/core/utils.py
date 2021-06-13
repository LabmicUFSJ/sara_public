"""
Utils
"""
import datetime
import logging
import re
import time
from pathlib import Path

import networkx as nx
import requests
from requests.exceptions import (ChunkedEncodingError, ConnectionError,
                                 ConnectTimeout, HTTPError, RequestException,
                                 SSLError, Timeout)

logging.basicConfig(filename='sara.log', level=logging.WARNING)


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
    """Get URL not shorted.

    Make a web request in return the URL complete.
    wait before multiple connections, be polite 2 seconds.
    """

    # polite
    time.sleep(1)
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)'
               ' AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/51.0.2704.103 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except (ConnectTimeout, Timeout) as error_msg:
        print(f'Error {error_msg}')
        logging.error('Error time out %s', error_msg)

        url_from_error = get_url_from_error(str(error_msg))
        if not url_from_error:
            return url
        if _is_valid(url_from_error):
            return url_from_error

        return url

    except (SSLError, HTTPError, ConnectionError) as error_msg:
        if 'Temporary failure in name resolution' in str(error_msg):
            print(f'Fail name resolution {error_msg}')
            logging.error('Error name resolution %s', error_msg)
            time.sleep(1)
            connection_attempt -= 1
            if connection_attempt:
                get_web_url(url, connection_attempt)
        logging.error('URL offline %s', url)
        url_from_error = get_url_from_error(str(error_msg))
        if not url_from_error:
            return url
        if _is_valid(url_from_error):
            return url_from_error
        return url

    except (RequestException, ChunkedEncodingError, Exception) as error:
        logging.error('General exception error %s', error)
        return url

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


def load_txt(path_to_file):
    """Load a txt from path and return list.

    Args:
        path_to_file ([type]): [description]
    """
    with open(path_to_file, "r") as lines:
        return [line.strip() for line in lines]
