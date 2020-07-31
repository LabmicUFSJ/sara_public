# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Central de Análise de conteúdo do Framework Sara.
Gera a Nuvem de palavras

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
"""
# import core.bagwords as bagwords
import sys

import sara.core.topic_model as topic_model

try:
    name = sys.argv[0]
    database = sys.argv[1]
    collection = sys.argv[2]
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Digite {name} <banco> <colecao>")
    sys.exit()

print(f"Banco a ser utilizado:{database} \nColecao: {collection}")


# Análise de conteúdo
words = topic_model.main(database, collection, 1000)
# print("Modelagem ... OK\nSentimento Modelagem:")
# print("Sentimento Modelagem... ok")
