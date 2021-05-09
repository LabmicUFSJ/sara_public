"""
Este módulo é responsavel pelo agendamento de coleta
"""

import sys
import sched
import time

from sara.core.sauron_coletor import Sauron
from sara.core.logger import log

coletor = Sauron()
agendamento = sched.scheduler(time.time, time.sleep)
intervalo = 0

try:
    name_file = sys.argv[0]
    termo = sys.argv[1]
    colecao = sys.argv[2]
    nome_banco = sys.argv[3]
    # em minutos
    msg_coleta = "Digite a duracão da coleta em minutos(Exemplo 10): "
    msg_intervalo = "Digite o intervalo entre as coletas(Exemplo 60): "
    duracao_coleta = float(input(msg_coleta))
    intervalo_coleta = float(input(msg_intervalo))

except IndexError as exc:
    print(f"error {exc}")
    print(f"ERRO!Digite {name_file} <termo> "
          "<colecao> <banco de dados>")
    print("\nTermo: O termo a ser coletado" +
          "\nColecao: A coleção onde os tweets serão salvos" +
          "\nBanco de Dados: O  banco onde os dados serão armazenados")

    sys.exit()


def coleta(termo, colecao, nome_banco, duracao):
    """Coleta de dados."""
    print("Realizando coleta agendada.")
    print(f"Duracao desta coleta {duracao} min ")
    log(termo)
    coletor.coleta_agendada(termo, colecao, nome_banco, duracao)
    print("Fim desta coleta.. aguardando nova coleta agendada.")
    print(f"Tempo até proxima coleta {intervalo_coleta} min.")


while True:
    agendamento.enter(intervalo*60, 1, coleta, argument=(termo, colecao,
                                                         nome_banco,
                                                         duracao_coleta))
    intervalo = intervalo_coleta
    agendamento.run()
