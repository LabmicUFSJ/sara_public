# Sara
[![experimental](https://img.shields.io/badge/stability-experimental-red)](https://github.com/LabmicUFSJ/sara_public/) [![version](https://img.shields.io/badge/version-0.3-blue)](https://github.com/LabmicUFSJ/sara_public/blob/master/CHANGELOG.md) [![labmic](https://img.shields.io/badge/UFSJ-Labmic-lightgrey)](https://ufsj.edu.br/)





A Sara é um framework semi-automatizado para coleta e análise de dados de redes sociais online, utilizando Redes complexas, Aprendizagem de Máquina e Mineração de texto.

Desenvolvido no Laboratório de Modelagem Computacional e Inteligência Computacional (LABMIC) da Universidade Federal de São João del-Rei (UFSJ)

Estado : Em desenvolvimento / Experimental

Site : https://labmicufsj.github.io/sara_public/



## Guias

- [Guia de Instalacão.](sara/Guias/Guia_instalacao.md)
- [Guia geral como utilizar.](sara/Guias/Guia_execucao.md)
- [Agendamento de Coleta.](sara/Guias/Guia_agendamento.md)

Módulos
-------

#### Coletor

O módulo de coleta utiliza a API do Twitter.

Módulos associados:
* `sara_coletor` - Realiza as coletas de tweets em tempo real.
* `coletor_agendado` - Realiza coletas de acordo com agendamento.
* `conexao_twitter` - Contém os dados de acesso da API do Twitter.

Os dados coletados são salvos no mongodb, um banco de dados não relacional.

#### Geração da Rede

A geração da rede é realizada por meio do módulo `sara_estrutural`.

* `sara_estrutural` - Gera uma rede direcionada ou não direcionada.

A rede gerada é salva no diretório `redes/`.

#### Análise de Centralidade

O framework identifica os vértices de maior importância de acordo com as seguintes métricas de centralidade:
- Betweenness, PageRank, Degree, Curtidas, Retweets.

A detecção de centralidade é realizada por meio da utilização do módulo sara_centralidade.

O resultado deste módulo é salvo no diretório `resultados_importancia/`.

#### Detecção de Comunidades

A detecção de comunidade neste framework é realizada por meio do módulo Overlap.

Esta ferramenta procura encontrar ego comunidades formada em torno de determinados usuários.

- Detecção de comunidades - Realiza a detecção de comunidades sobrepostas, utilize o resultado da centralidade ou outra sequência de importância para detecção de comunidades.

Modulo associado

- `overlap.py`

#### Análise de conteúdo

A visualização e análise do conteúdo é realizada por meio da utilização da técnica de LDA combinada com uma nuvem de palavras.

Módulos associados:

* `Sara_conteudo` - Responsável pela geração da nuvem de palavras.
* `Sara_sentimento` - Responsável pela análise de sentimento.


## Dependências:

Consulte o guia de instalação.
- python >= 3.6
- pymongo
- mongodb
- networkx
- gensim
- spacy
- matplot
- wordcloud
- nltk
- seaborn
- pandas

## Artigos associados

Trabalhos relacionados a esta pesquisa que foram publicados em conferências:

- [Sara - A Semi-Automatic Framework for Social Network Analysis](https://sol.sbc.org.br/index.php/webmedia_estendido/article/view/8137/8012)

- [A framework for the analysis of information propagation in social networks combining complex networks and text mining techniques full strip](https://dl.acm.org/doi/abs/10.1145/3323503.3360289)
