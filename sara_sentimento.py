# -*- coding: utf-8 -*-
"""
Módulo Responsável pela Análise de sentimento
Utiliza o Leia para realizar a análise Léxica de Sentimento.
"""
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import sara.core.database as bd
from sara.sentimento.leia import SentimentIntensityAnalyzer
from sara.core.config import sentiment_path
from sara.core.utils import check_path

# Check if path exist.
check_path(sentiment_path)


class DetectorSentimento():
    """ Realiza a análise de sentimento Léxica."""
    def __init__(self):
        self.leia = SentimentIntensityAnalyzer()

    @staticmethod
    def sentimento(score):
        """aux score de sentimento."""
        if score >= 0.5:
            return 1
        if score <= -0.5:
            return -1
        return 0

    def main(self, banco_dados, colecao):
        """Recebe como parâmetro o nome do banco e da colecao."""
        tweets = bd.carrega_tweet_mongo(banco_dados, colecao)
        sentimento = []
        sentimento_final = []
        final = []
        for i in tweets:
            resultado = self.leia.polarity_scores(i)
            if resultado['compound'] > 0:
                sentimento.append(resultado['compound'])
                sentimento_final.append("Positivo")
                final.append(1)
            elif resultado['compound'] < 0:
                sentimento.append(resultado['compound'])
                sentimento_final.append("Negativo")
                final.append(-1)
            else:
                sentimento.append(resultado['compound'])
                sentimento_final.append("Neutro")
                final.append(0)

        tupla = list(zip(tweets, sentimento, sentimento_final, final))
        data_frame = pd.DataFrame(tupla, columns=['Tweet',
                                                  'Indice',
                                                  'Sentimento', 'Final'])

        print("Sentimento\n", data_frame.Sentimento.value_counts())
        data_frame.Sentimento.value_counts().to_csv(f"{sentiment_path}"
                                                    f"analise_sentiment_resumo"
                                                    f"{colecao}.csv")
        data_frame.to_csv(f"{sentiment_path}analise_sentiment{colecao}.csv",
                          index=False)

        fig, axes = plt.subplots(figsize=(7, 7))
        axes = sns.countplot(y="Sentimento", data=data_frame, ax=axes)
        plt.show()
        fig.savefig("last_analise.png")


# --- chamada ----
detecta_sentimento = DetectorSentimento()

try:
    name_file = sys.argv[0]
    database_name = sys.argv[1]
    collection = sys.argv[2]
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Digite {name_file} <banco> <colecao>")
    sys.exit()
detecta_sentimento.main(database_name, collection)
