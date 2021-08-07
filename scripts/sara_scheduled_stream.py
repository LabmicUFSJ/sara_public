"""
Este módulo é responsavel pelo agendamento de coleta
"""

import sys
import sched
import time

from sara.core.collector import SaraCollector
from sara.core.logger import log
from sara.core.sara_data import SaraData


def handler_input():
    """Handler user input."""
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

        sys.exit(-1)
    return termo, colecao, nome_banco, duracao_coleta, intervalo_coleta


def coleta(termo, duracao, coletor, intervalo):
    """Coleta de dados."""
    print("Realizando coleta agendada.")
    print(f"Duracao desta coleta {duracao} min ")
    log(termo)
    coletor.scheduled(termo, duracao)
    print("Fim desta coleta.. aguardando nova coleta agendada.")
    print(f"Tempo até proxima coleta {intervalo} min.")


def main():
    """Main."""
    termo, colecao, nome_banco, duracao, intervalo_coleta = handler_input()
    storage = SaraData(colecao, nome_banco)
    coletor = SaraCollector(storage)
    agendamento = sched.scheduler(time.time, time.sleep)
    intervalo = 0
    while True:
        agendamento.enter(intervalo*60, 1, coleta, argument=(termo,
                                                             duracao,
                                                             coletor,
                                                             intervalo_coleta))
        intervalo = intervalo_coleta
        agendamento.run()


if __name__ == '__main__':
    main()
