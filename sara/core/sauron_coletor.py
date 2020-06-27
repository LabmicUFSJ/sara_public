# -*- coding: utf-8 -*-
"""
Modulo de coleta utilizando a api do Twitter .
"""
# import codecs
# import os
# import sys

import sys
import time

from sara.credenciais.conexao_twitter import inicia_conexao
from pymongo import MongoClient
from twitter.error import TwitterError
from http.client import IncompleteRead
import threading
import queue
from sara.core.logger import log_erro

fila = queue.Queue()


def processa_fila():
    """Consulta a fila e salva os dados no banco."""
    while True:
        tweet, conexao = fila.get()
        conexao.replace_one(tweet, tweet, True)
        fila.task_done()


threading.Thread(target=processa_fila, daemon=True).start()


class Sauron():
    """Classe responsavel pela coleta de dados ."""

    def __init__(self):
        # conexão com o banco de dados
        self.cliente = MongoClient('localhost', 27017)

        # inica a conexao com twitter
        self.api = inicia_conexao()
        # caminho = 'central_eleicoes/'
        # configuração do banco de dados MongoDB
        self.controle_exibicao = 1000
        self.sleep_on_error = 20

    def banco(self, nome_banco, colecao):
        """configura collection e db"""
        # # configura o local de salvamento no banco.
        banco = self.cliente[nome_banco]
        # coleção ...
        post = banco[colecao]
        return post

    @staticmethod
    def escreve_lista(nome_arquivo, lista):
        """Escreve no arquivo"""
        arq = open(nome_arquivo, "w")
        for i in lista:
            arq.write(str(i))
            arq.write('\n')
        arq.close()

    def save_data(self, name, data):
        """save data to file json"""
        arq = open(name + ".txt", "a")
        arq.write(str(data))
        arq.write("\n")
        arq.close()

    def salvar_mongo(self, tweet, post):
        """Salva o tweet no mongodb"""
        post.replace_one(tweet, tweet, True)
        # self.save_data("dados_coletados", tweet)

    def coleta_agendada(self, termo_pesquisa, colecao, nome_banco, duracao):
        """Coleta com agendamento."""
        conexao_banco = self.banco(nome_banco, colecao)
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
                # self.salvar_mongo(tweet, conexao_banco)
                # coloca na fila para processamento dos dados
                fila.put((tweet, conexao_banco))
        except (TwitterError, IncompleteRead) as exc:
            print(f"error {exc.message}")
            log_erro(exc.message)
            if 'Unauthorized' in exc.message.get('message'):
                print("favor verificar as credências de acesso.")
                sys.exit()
            time.sleep(self.sleep_on_error)
            # realiza coleta no período de tempo restante
            restante = break_after-time.time()
            self.coleta_agendada(termo_pesquisa, colecao, nome_banco,
                                 restante)

    def monitor_twitter(self, termo_pesquisa, conexao_banco, limite=0):
        """Monitora as postagens em tempo real"""
        # print("TP",termo_pesquisa,"Limite",limite)
        retorno = self.api.GetStreamFilter(track=[termo_pesquisa])
        # print(list(retorno))
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
                # self.salvar_mongo(tweet, conexao_banco)
                # coloca em uma fila para processamento
                fila.put((tweet, conexao_banco))
                if contador == limite and limite != 0:
                    print("Coleta encerrada a partir do limite determinado.")
                    return
        except (TwitterError, IncompleteRead) as exc:
            print(f"error {exc.message}")
            log_erro(exc.message)
            if 'Unauthorized' in exc.message.get('message'):
                print("favor verificar as credencias de acesso.")
                sys.exit()
            time.sleep(self.sleep_on_error)
            self.monitor_twitter(termo_pesquisa, conexao_banco, limite)

    def obtem_ids(self, lista_nomes):
        """Obtém ids de uma lista de nomes"""
        lista_ids = []
        for name in lista_nomes:
            try:
                info = self.api.GetUser(screen_name=name)
                id = info._json['id']
                lista_ids.append([name, id])
            except Exception as exc:
                print(name + '\n')
                print(f"error {exc}")
        return lista_ids

    veiculos = [
        '@uol',
        '@uolnoticias',
        '@g1',
        '@veja',
        '@brasil247',
        '@cartacapital',
        '@exame',
        '@elpais_brasil',
        '@bbcbrasil',
        '@RevistaEpoca',
        '@folha',
        '@veja',
        '@estadao',
        '@tijolaco',
        '@o_antagonista',
        '@agenciabrasil',
    ]

    checadores_noticias = ['@agencialupa', '@aosfatos', '@agenciapublica']

    # nome da coleção
    def pesquisa(self, padrao_pesquisa, limite, colecao, nome_banco="eleicao"):
        """método de pesquisa"""
        print("Padrão de Busca:", padrao_pesquisa)
        print("Collection Onde os dados serão salvos?:", colecao)
        post = self.banco(nome_banco, colecao)
        self.monitor_twitter(padrao_pesquisa, post, limite)
