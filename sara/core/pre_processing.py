# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Aplica o pré-processamento
Pre-processing
"""
# import ast
import re
# import base
import string
from collections import Counter
from unicodedata import normalize

import emoji
import spacy
import sara.stopWords.StopWords as stopWords

# print('spaCy Version: %s' % (spacy.__version__))
nlp = spacy.load("pt_core_news_sm")
spacy_stopwords = spacy.lang.pt.stop_words.STOP_WORDS
set_stop = stopWords.load_stop_words()
# carrega adjetivos
set_adjetivos = stopWords.load_stop_words("adjetivos.txt")
# combina as duas bases de stopWords
set_stop = set_stop.union(spacy_stopwords)
set_stop = set_stop.union(set_adjetivos)


def remove_emoji(text):
    """remove emoji de uma string."""
    return emoji.get_emoji_regexp().sub(u'', text)


def to_int_str(data):
    """converte para inteiro."""
    return str(int(data))


def tolower(lista):
    """converte os elementos na lista para minusculo."""
    list_lower = []
    for i in lista:
        list_lower.append(i.lower())
    return list_lower


def save_data(name, data):
    """save data to file json"""
    arq = open(name + ".txt", "a")
    arq.write(str(data))
    arq.write("\n")
    arq.close()


def remover_acentos(txt):
    """remove acentuação."""
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def common_words(tokens):
    """common_words find"""
    counter = Counter(tokens)
    most_occur = counter.most_common(100)
    print("Common words in your text")
    print(most_occur)
    return most_occur


def formata_data(old_date):
    """formata data"""
    data = old_date.split("/")
    new_data = (
        to_int_str(data[1])
        + "/"
        + to_int_str(data[0])
        + "/"
        + to_int_str(data[2])
    )
    return new_data


def remove_user_mention(text):
    """remove user mention, @username"""
    if re.search(r"(@)\S*", text):
        text = re.sub(r"(@)\S*", " ", text)
    return text


def find_link(text):
    """remove links"""
    text = re.sub(r"(pic.twitter)\S*", " ", text)
    if re.search(r"(https:)\S*", text):
        # print(f"Link found in: {text}")
        text = re.sub(r"(https:)\S*", " ", text)
        # print("t",text)
        text = text.replace("...", "")
    elif re.search(r"(http:)\S*", text):
        text = re.sub(r"(http:)\S*", " ", text)
    return text


def pre_processing(text):
    """Aplica o pré-processamento no texto."""
    # convert text to lowercase
    text = text.lower()
    # find links
    text = find_link(text)
    # remove user mention
    text = remove_user_mention(text)
    # remove number in text
    text = re.sub(r"\d+", " ", text)
    # remove smiles type kkk
    text = re.sub(r"(kk)+\s", " ", text)
    # remove broken words
    text = re.sub(r"\s[\w]{1}\s", " ", text)
    # remove punctuation
    text = re.sub('[' + string.punctuation + ']', " ", text)
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
    tokens_final = [i for i in token_list if i not in set_stop]
    return " ".join(tokens_final)


# Processa os textos


def main(all_textos):
    common_list = []
    cont = 0
    final_list = []
    for i in all_textos:
        print("Working ", cont, "/", len(all_textos))
        cont += 1
        # Realiza a limpeza do campo de texto, os demais campos sao mantidos
        after = pre_processing(i['texto'])
        merge = " ".join(after)
        i['texto'] = merge

        # Realiza o tratamento dos demais campos
        i['empresa'] = i['empresa'].lower()
        i['topicos'] = tolower(i['topicos'])
        i['local'] = i['local'].lower()
        i['titulo'] = i['titulo'].lower()

        # adiciona a empresa limpa em uma lista final
        final_list.append(i)

        # lista nomes comuns
        common_list = common_list + after
        # save_data(NAME_FILE+"_processado",merge)
    print("Pré-processamento completo")
    print("Aplicando common words em todo o texto")
    common = common_words(common_list)
    return final_list, common
    # common={"mes":MONTH,"common_words":common_list}
    # con_colecao=base.iniciar_colecao(cliente,"common_words")
    # con_colecao.replace_one(common,common,True)
