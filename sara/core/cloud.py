# encode: utf-8
"""
Módulo geração nuvem de palavras
Generate cloud words.
"""
import uuid

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from sara.core.config import cloud_path
from sara.core.utils import create_path

# Create a path
create_path(cloud_path)


# def black_color(word, font_size, position, orientation, random_state=None,
#                 **kwargs):
#     return "hsl(0, 100%,1%)"

def black_color(**_):
    """Return color."""
    return "hsl(0, 100%,1%)"


def _unpack(texto, n_repeticoes):
    """Unpack."""
    texto_str = ""
    print("LDA")
    for i in texto:
        texto_str += " " + str(i[1])
        for _ in range(0, int(i[0]*n_repeticoes)):
            palavra = i[1].replace(" ", "_")
            texto_str += " "+str(palavra)

    return texto_str


def make_cloud(texto, name):
    """Generate words cloud."""
    # Generate a word cloud image
    wordcloud = WordCloud(height=300, width=800,
                          max_font_size=40, margin=1, min_font_size=2,
                          collocations=False,
                          background_color="white").generate(texto)

    # Display the generated image:
    plt.title(f"Análise {name}")
    wordcloud.recolor(color_func=black_color, random_state=0)
    # name_pdf = f"{cloud_path}cloud_{name}_{str(uuid.uuid4().hex)}.pdf"
    name_svg = f"{cloud_path}cloud_{name}_{str(uuid.uuid4().hex)}.svg"
    # save pdf
    # wordcloud.to_file(name_pdf)
    data = wordcloud.to_svg()
    # save svg
    with open(name_svg, "w") as arq:
        arq.write(data)

    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # # get current figure
    # fig = plt.gcf()
    # fig.set_size_inches(10, 10)
    # # plt.savefig(f"{cloud_path}cloud_{name}_{str(uuid.uuid4().hex)}.svg")
    # # plt.savefig(f"{cloud_path}cloud_{name}_{str(uuid.uuid4().hex)}.pdf",
    # #             dpi=1300)
    # plt.show()


def cloud_lda(lista_tweets, n_repeticoes=1000):
    """Gera a nuvem de tags a partir de uma lista de tuplas LDA."""
    print("REP", n_repeticoes)
    texto = _unpack(lista_tweets, n_repeticoes)
    # texto="casarao_casa casa_casinha"
    make_cloud(texto, "lda")
    print("Cloud Lda Gerada.!!")
