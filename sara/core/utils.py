"""
Módulo de utilidades.
"""
import re
import datetime
import os


def max_data_tweets(tweets):
    """Retorna a data de postagem mais nova dos tweets."""
    anos = []
    for tweet in tweets:
        try:
            # print(tweet.get('id'))
            ano = tweet.get('created_at')
            year = re.sub(r"[+].\d*", " ", ano)
            year = year.replace("  ", "")
            date1 = datetime.datetime.strptime(year, '%a %b %d %H:%M:%S %Y')
            date1 = date1.strftime("%Y-%m-%d")
            anos.append(date1)
        except KeyError:
            pass
    return max(anos)


def check_path(dir):
    """Create a dir."""
    if os.path.exists(dir) is False:
        os.mkdir(dir)
        print(f"Diretório {dir} foi criado.")
