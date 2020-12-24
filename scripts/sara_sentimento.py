# -*- coding: utf-8 -*-
"""
Módulo Responsável pela Análise de sentimento
Utiliza o Leia para realizar a análise Léxica de Sentimento.
Sentimental Analysis

Sara - Sistema de Análise de Dados de Redes Sociais Online
Licença - MIT
Autores: Carlos Magno
LABMIC - UFSJ
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


class SentimentAnalysis():
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

    def main(self, database, collection):
        """Recebe como parâmetro o nome do banco e da colecao."""
        tweets = bd.carrega_tweet_mongo(database, collection)
        sentiment = []
        sentiment_final = []
        final = []
        for i in tweets:
            resultado = self.leia.polarity_scores(i)
            if resultado['compound'] > 0:
                sentiment.append(resultado['compound'])
                sentiment_final.append("Positivo")
                final.append(1)
            elif resultado['compound'] < 0:
                sentiment.append(resultado['compound'])
                sentiment_final.append("Negativo")
                final.append(-1)
            else:
                sentiment.append(resultado['compound'])
                sentiment_final.append("Neutro")
                final.append(0)

        tupla = list(zip(tweets, sentiment, sentiment_final, final))
        data_frame = pd.DataFrame(tupla, columns=['Tweet',
                                                  'Indice',
                                                  'Sentimento', 'Final'])

        print("Sentimento\n", data_frame.Sentimento.value_counts())
        data_frame.Sentimento.value_counts().to_csv(f"{sentiment_path}"
                                                    f"analise_sentiment_resumo"
                                                    f"{collection}.csv")
        data_frame.to_csv(f"{sentiment_path}analise_sentiment{collection}.csv",
                          index=False)

        fig, axes = plt.subplots(figsize=(7, 7))
        axes = sns.countplot(y="Sentimento", data=data_frame, ax=axes)
        plt.show()
        fig.savefig("last_analise.png")


# --- chamada ----
sentiment_analisys = SentimentAnalysis()

try:
    name = sys.argv[0]
    database = sys.argv[1]
    collection = sys.argv[2]
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Digite {name} <banco> <colecao>")
    sys.exit()
sentiment_analisys.main(database, collection)
