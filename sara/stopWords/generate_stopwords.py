from collections import Counter
from unicodedata import normalize

"""
Gerador de lista de stopwords
Combina diferentes bases e analisa os termos mais frequentes do texto.
"""


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


# leitura dos arquivos
arquivo = open("gerador_stop_words.txt")


lista_final = []
for i in arquivo:
    lista_final.append(i)

lista_stop_words = []
# elimina elementos duplicados.
lista_unica = set(lista_final)
for i in lista_unica:
    lista_stop_words.append(i.strip().lower())

sem_acentuacao = lista_stop_words.copy()
lista_sem_acentuacao = []
for i in sem_acentuacao:
    lista_sem_acentuacao.append(remover_acentos(i))
lista_stop_words = set(lista_stop_words).union(set(lista_sem_acentuacao))
print(len(lista_stop_words))
arquivo.close()
arq = open("sara/stopwords_v2.txt", "w")
for i in lista_stop_words:
    arq.write(i + "\n")
arq.close()


def palavras_frequentes(base_completa):
    all = []
    for i in base_completa:
        all.append(i['texto'])

    texto_completo = " ".join(all)
    texto_partido = texto_completo.split()
    counter = Counter(texto_partido)

    most_occur = counter.most_common(100)
    print(most_occur)
