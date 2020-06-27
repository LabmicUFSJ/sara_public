# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central Estrutural -
Sara - Sistema de Análise de Dados com Redes Complexas e Analytics
Focado em análises politicas no twitter.
Geração da rede
"""
# system import
import sys

# intern import
import sara.core.rede_retweets as rede


def main():
    """Inicia a geração da rede."""
    try:
        nome_rede = sys.argv[1]
        nome_base = sys.argv[2]
        nome_colecao = sys.argv[3]
        direcionada = sys.argv[4]
        limite = int(sys.argv[5])
        # limite de tweets a serem utilizados
    except IndexError as exc:
        print(f"erro {exc}")
        print("ERRO!!\nDigite:\n>python3 saraEstrutural.py <nome_rede>"
              " <nome_base> <nome_colecao> <True||False> <limite>")
        print("True: Rede direcionada, False: Rede não direcionada"
              "\nlimite:0 para utilizar a base completa")
        sys.exit()
    print(f"Dados digitados\n Nome Grafo:{nome_rede}\n banco:{nome_base}\n"
          f" Colecao:{nome_colecao}\n Direcionada:{direcionada}\n "
          f"Limite de tweets:{limite}")

    rede.main(nome_rede, nome_base,
              nome_colecao, direcionada, limite)


if __name__ == '__main__':
    main()
