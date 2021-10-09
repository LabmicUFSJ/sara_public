"""
Script to schedule real time tweets collect.
SARA - Framework

"""

import sched
import sys
import time

from sara.core.collector import SaraCollector
from sara.core.logger import keyword_log
from sara.core.sara_data import SaraData


def handler_input():
    """Handler user input."""
    try:
        name_file = sys.argv[0]
        keyword = sys.argv[1]
        collection = sys.argv[2]
        database = sys.argv[3]
        # em minutos
        msg_collect = ("Duration the window to collect tweets in minutes "
                       "(Example 10): ")
        msg_window = "Time between windows (Example 60): "
        duracao_coleta = float(input(msg_collect))
        intervalo_coleta = float(input(msg_window))

    except IndexError as exc:
        print(f"Error {exc}")
        print(f"ERRO!Plase input python {name_file} <keyword> "
              "<collection> <database>")
        print("\nkeyword: The keyword will be collected." +
              "\nCollection: Collection where these tweets will be stored" +
              "\nDatabase: The database where this tweets will be stored")

        sys.exit(-1)
    return keyword, collection, database, duracao_coleta, intervalo_coleta


def get_tweets(keyword, duration, colector, interval):
    """Get tweets from real time stream."""
    print("Making scheduled collect.")
    print(f"Time these window {duration} min ")
    keyword_log(keyword)
    colector.scheduled(keyword, duration)
    print("End.. waiting next window to collect tweets.")
    print(f"Time to next windo {interval} min.")


def main():
    """Main."""
    keyword, collection, database_name, duration, wait = handler_input()
    storage = SaraData(collection, database_name)
    colector = SaraCollector(storage)
    schedule = sched.scheduler(time.time, time.sleep)
    interval = 0
    while True:
        schedule.enter(interval*60, 1, get_tweets, argument=(keyword,
                                                             duration,
                                                             colector,
                                                             wait))
        interval = wait
        schedule.run()


if __name__ == '__main__':
    main()
