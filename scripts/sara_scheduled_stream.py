"""
Script to schedule real time tweets collect.
SARA - Framework

"""

import sched
import sys
import time

from sara.core.collector import SaraCollector
from sara.core.logger import log
from sara.core.sara_data import SaraData


def handler_input():
    """Handler user input."""
    try:
        name_file = sys.argv[0]
        term = sys.argv[1]
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
        print(f"ERRO!Plase input python {name_file} <term> "
              "<collection> <database>")
        print("\nTerm: The term will be collected." +
              "\nCollection: Collection where these tweets will be stored" +
              "\nDatabase: The database where this tweets will be stored")

        sys.exit(-1)
    return term, collection, database, duracao_coleta, intervalo_coleta


def get_tweets(term, duration, colector, interval):
    """Get tweets from real time stream."""
    print("Making scheduled collect.")
    print(f"Time these window {duration} min ")
    log(term)
    colector.scheduled(term, duration)
    print("End.. waiting next window to collect tweets.")
    print(f"Time to next windo {interval} min.")


def main():
    """Main."""
    term, collection, database_name, duration, coll_interval = handler_input()
    storage = SaraData(collection, database_name)
    colector = SaraCollector(storage)
    schedule = sched.scheduler(time.time, time.sleep)
    interval = 0
    while True:
        schedule.enter(interval*60, 1, get_tweets, argument=(term,
                                                             duration,
                                                             colector,
                                                             coll_interval))
        interval = coll_interval
        schedule.run()


if __name__ == '__main__':
    main()
