# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import spacy
import stopWords.StopWords as stopWords
from unicodedata import normalize
import re
import base
import string
from collections import Counter

"""
Aplica o pré-processamento e salva a base completa
"""
cliente = base.iniciar_conexao()
con_colecao = base.iniciar_colecao(cliente, "colecao_processada")


def load_base():
    all_textos = base.carrega_colecao_completo(
        "brumadinhoinflux", "colecao_completa"
    )
    return all_textos


# print('spaCy Version: %s' % (spacy.__version__))
spacy_nlp = spacy.load('pt')
nlp = spacy.load("pt_core_news_sm")
spacy_stopwords = spacy.lang.pt.stop_words.STOP_WORDS
set_stop = stopWords.load_stop_words()
# combina as duas bases de stopWords
set_stop.union(spacy_stopwords)

all_textos = load_base()


def to_int_str(data):
    return str(int(data))


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def common_words(tokens):
    """common_words find"""
    counter = Counter(tokens)
    most_occur = counter.most_common(100)
    print("Common words in your text")
    print(most_occur)


def formata_data(old_date):
    data = old_date.split("/")
    new_data = (
        to_int_str(data[1])
        + "/"
        + to_int_str(data[0])
        + "/"
        + to_int_str(data[2])
    )
    return new_data


def pre_processing(text):
    # convert text to lowercase
    text = text.lower()
    # remove number in text
    text = re.sub(r"\d+", " ", text)
    # remove broken words
    text = re.sub("r\s[\w]{1}\s", " ", text)
    # remove punctuation
    text = re.sub('[' + string.punctuation + ']', ' ', text)
    # White spaces removal
    text = text.strip()
    # remove accents
    text = remover_acentos(text)
    # generate tokens
    token_list = []
    tokens = nlp(text)
    for token in tokens:
        word = re.sub(r"\s", "", token.text)
        if len(word) > 1:
            token_list.append(word)
    # remove stopwords
    tokens_final = [i for i in token_list if not i in set_stop]
    return tokens_final


common_list = []
cont = 0
for i in all_textos:
    print("Working ", cont, "/", len(all_textos))
    cont += 1
    after = pre_processing(i['texto'])
    merge = " ".join(after)
    new_data = formata_data(i['data'])
    i.update({"data": new_data})
    i.update({"texto": merge})
    common_list = common_list + after
    con_colecao.replace_one(i, i, True)
print("Pré-processamento completo")
print("Aplicando common words em todo o texto")
common_words(common_list)
common = {"common_words": common_list}
con_colecao = base.iniciar_colecao(cliente, "common_words")
con_colecao.replace_one(common, common, True)
cliente.close()
