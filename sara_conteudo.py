# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central de Análise de conteúdo do Framework Sara.
Gera a Núvem de palavras
"""
# import core.bagwords as bagwords
import sys

import sara.core.modelagem_topicos as modelagem_topicos

try:
    name_file = sys.argv[0]
    banco = sys.argv[1]
    colecao = sys.argv[2]
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Digite {name_file} <banco> <colecao>")
    sys.exit()

print(f"Banco a ser utilizado:{banco} \nColecao: {colecao}")


# Análise de conteúdo
palavras = modelagem_topicos.main(banco, colecao, 1000)
# print("Modelagem ... OK\nSentimento Modelagem:")
# print("Sentimento Modelagem... ok")
