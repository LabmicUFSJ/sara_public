# -*- coding: utf-8 -*-
"""
Modulo de coleta utilizando a api do Twitter .
"""

import sys
import time

from requests.exceptions import ChunkedEncodingError
from twitter.error import TwitterError
from urllib3.exceptions import IncompleteRead, ProtocolError

from sara.core.logger import log_erro
from sara.core.sara_data import SaraData
from sara.credentials.twitter_api import get_twitter_api


class SaraCollector():
    """Classe responsavel pela coleta de dados ."""

    def __init__(self, storage):
        # inica a conexao com twitter
        self.api = get_twitter_api()
        # configuração do banco de dados MongoDB
        self.controle_exibicao = 1000
        self.sleep_on_error = 10
        if not isinstance(storage, SaraData):
            raise TypeError('The Storage type is necessary.')
        self.storage = storage

    def scheduled(self, termo_pesquisa, duracao):
        """Scheduled collector."""
        retorno = self.api.GetStreamFilter(track=[termo_pesquisa])
        contador = 0
        exibicao = 0
        now = time.time()
        break_after = (duracao*60) + now
        try:
            for tweet in retorno:
                if time.time() >= break_after:
                    print("Tweets Coletados", contador)
                    return
                if exibicao == self.controle_exibicao:
                    print("Tweets Coletados", contador)
                    exibicao = 0
                contador += 1
                exibicao += 1
                # coloca na fila para processamento dos dados
                self.storage.save_data((tweet))
        except (TwitterError, ProtocolError, IncompleteRead,
                ChunkedEncodingError) as exc:
            print(f"error {exc.message}")
            log_erro(exc.message)
            if 'Unauthorized' in exc.message:
                print(f"Please check your credentials {exc.message}.")
                sys.exit(-1)

            # Wait X seconds to try to collect new tweets again.
            time.sleep(self.sleep_on_error)
            # realiza coleta no período de tempo restante
            restante = break_after-time.time()
            self.scheduled(termo_pesquisa, restante)

    def real_time_collector(self, termo_pesquisa, limite=0):
        """Monitora as postagens em tempo real"""
        retorno = self.api.GetStreamFilter(track=[termo_pesquisa])
        print("Coletando dados", "Termo:", termo_pesquisa)
        contador = 0
        exibicao = 0
        try:
            for tweet in retorno:
                if exibicao == self.controle_exibicao:
                    print("Tweets Coletados", contador)
                    exibicao = 0
                contador += 1
                exibicao += 1
                self.storage.save_data((tweet))
                if contador == limite and limite != 0:
                    print("Coleta encerrada a partir do limite determinado.")
                    return
        except (TwitterError, ProtocolError, IncompleteRead,
                ChunkedEncodingError) as exc:
            print(f"error {exc.message}")
            log_erro(exc.message)
            if 'Unauthorized' in exc.message:
                print(f"Please check your credentials {exc.message}.")
                sys.exit(-1)
            # wait to retry collect tweets.
            time.sleep(self.sleep_on_error)
            self.real_time_collector(termo_pesquisa, limite)

    def collector_followers(self, user_id):
        """collector followers from a user_id."""
        next_cursor = -1
        new_list = []
        while True:
            data = self.api.GetFollowersPaged(user_id=user_id,
                                              cursor=next_cursor)
            next_cursor, previous, users = data
            new_list = list(set(new_list+users))
            if len(users) < 200:
                break
        name = str(user_id)+'.json'
        print(name, len(new_list))
        for user in new_list:
            self.storage.save_data_file(name, user.AsDict())
        print(previous, next_cursor)
