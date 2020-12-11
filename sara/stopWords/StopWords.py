# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Load stopWords
"""


def load_stop_words(nome_padrao="stopwords_v2.txt"):
    """Load stopwords list, return a set"""
    try:
        with open(nome_padrao, "r") as arquivo:
            dados = arquivo.readlines()
    except Exception:
        complemento = "sara/stopWords/"
        with open(complemento+nome_padrao, "r") as arquivo:
            dados = arquivo.readlines()
    # lista_palavras=[]
    set_palavras = set()
    for i in dados:
        # lista_palavras.append(i.strip())
        set_palavras.add(i.strip())
    return set_palavras
