# encode: utf-8
"""
Módulo geração nuvem de palavras
Generate cloud words.
"""
import uuid

import matplotlib.pyplot as plt

from wordcloud import WordCloud
from sara.core.config import cloud_path
from sara.core.utils import check_path

# Check if path exist.
check_path(cloud_path)


def reorganiza(palavra):
    """transforma texto."""
    partes = palavra.split("_")
    retorno = "_".join(partes[::-1])
    return retorno


def gerar_texto(texto, n_repeticoes, lda=False):
    """Transforma a tupla em uma string."""
    # print(texto)

    texto_str = ""
    if(lda is False):
        for i in texto:
            for j in range(0, int(i[1] * n_repeticoes)):
                texto_str += " " + str(i[0])
    else:
        print("LDA")
        for i in texto:
            texto_str += " " + str(i[1])
            for j in range(0, int(i[0]*n_repeticoes)):
                # trecho que torna a palavra composta
                palavra = i[1].replace(" ", "_")
                texto_str += " "+str(palavra)
            # ---------------
            # sem bigrama

    return texto_str


def make_cloud(texto, name):
    """Cria a nuvem de tags."""
    # Generate a word cloud image
    wordcloud = WordCloud(collocations=False,
                          background_color="white").generate(texto)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f"{cloud_path}cloud_{name}_{str(uuid.uuid4().hex)}.png")
    # plt.show()


def cloud_tf(lista_tupla, n_repeticoes=1000):
    """Gera a nuvem de tags a partir de uma lista de tuplas."""
    print("TF")
    texto = gerar_texto(lista_tupla, n_repeticoes)
    make_cloud(texto, "tf_idf")
    print("Cloud Tf-idf Gerada!!")


def cloud_lda(lista_tweets, n_repeticoes=1000):
    """Gera a nuvem de tags a partir de uma lista de tuplas LDA."""
    print("REP", n_repeticoes)
    texto = gerar_texto(lista_tweets, n_repeticoes, True)
    # texto="casarao_casa casa_casinha"
    make_cloud(texto, "lda")
    print("Cloud Lda Gerada.!!")
