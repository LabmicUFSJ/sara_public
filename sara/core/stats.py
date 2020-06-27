"""
Gera estatistica basica sobre os usuários.
"""
from database import carregar_usuarios, carrega_tweets
from utils import max_data_tweets
from collections import Counter
import pandas as pd
from get_stats_perfil import estatistica
import seaborn as sns
import matplotlib.pyplot as plt

base = "mestrado"
colecao = "stf"
# from scipy.stats import norm

# banco = input("Digite o nome da variavel: ")
# print(f"você digitou {banco}")

# exit()
usuarios = carregar_usuarios(base, colecao)

tweets = carrega_tweets(base, colecao)
print(len(tweets))

data_coleta = max_data_tweets(tweets)
anos = []
metadados = []
for usuario in usuarios:
    try:
        metadadado = estatistica(usuario, data_coleta)
        ano = usuario.get('created_at').split(" ")[-1]
        anos.append(ano)
        metadados.append(metadadado)

    except KeyError:
        pass

table = pd.DataFrame(metadados)
table.to_csv("metadados.csv", index=False)
# print(table.describe())

# ax = sns.scatterplot(x="total_tweets", y="tweets_dia", data=table)
# plt.show()
# exit()

distribuicao = Counter(anos)
print(distribuicao)
print(distribuicao.most_common(3))
print(len(anos))
plt.title("Análise Ano de Criação das Contas")
plt.ylabel('Número de Contas')
plt.xlabel('Ano de Criação')
ax = sns.countplot(anos)
plt.show()
