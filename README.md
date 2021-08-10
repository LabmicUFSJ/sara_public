# SARA

[![experimental](https://img.shields.io/badge/stability-experimental-red)](https://github.com/LabmicUFSJ/sara_public/) [![version](https://img.shields.io/badge/version-0.2-blue)](https://github.com/LabmicUFSJ/sara_public/blob/master/CHANGELOG.md) [![labmic](https://img.shields.io/badge/UFSJ-Labmic-lightgrey)](https://ufsj.edu.br/)
[![Build Python Package](https://github.com/LabmicUFSJ/sara/actions/workflows/main.yml/badge.svg)](https://github.com/LabmicUFSJ/sara/actions/workflows/main.yml)
[![Tests and Linter](https://github.com/LabmicUFSJ/sara/actions/workflows/python-package.yml/badge.svg)](https://github.com/LabmicUFSJ/sara/actions/workflows/python-package.yml)

A SARA é um framework semi-automatizado para coleta e análise de dados de
redes sociais online (RSO), utilizando redes complexas, aprendizagem de máquina
e mineração de texto.

Desenvolvido no Laboratório de Modelagem Computacional e Inteligência Computacional (LABMIC) da Universidade Federal de São João del-Rei (UFSJ)

Estado : Em desenvolvimento / Experimental

Site : https://labmicufsj.github.io/sara_public/

## Guias

- [Guia geral como utilizar.](sara/guides/Guia_execucao.md)
- [Agendamento de Coleta.](sara/guides/Guia_agendamento.md)

## Instalação

Após criar um ambiente virtual execute:

``` console
pip install --upgrade wheel setuptools pip
```

### Instalando com Wheel

**Método de instalação recomendado**

``` console
python setup.py bdist_wheel && pip install --force-reinstall dist/*.whl

```

### Instale utilizando setup.py

``` console
python3 setup.py install
```

## Módulos

### Coletor

O módulo de coleta utiliza a API do Twitter.

Módulos associados:

- [`sara_stream`](scripts/sara_stream.py) - Realiza as coletas de tweets em tempo real.
- [`sara_scheduled_stream`](scripts/sara_scheduled_stream.py) - Realiza coletas de acordo com agendamento.
- [`credentials/twitter_api`](sara/credentials/twitter_api.py) - Contém os dados de acesso da API do Twitter.

Os dados coletados são salvos no mongodb, um banco de dados não relacional.

### Geração da Rede

A geração da rede é realizada utilizando o módulo `network_generators`.

Scripts:

- [`sara_network`](/scripts/sara_network.py) - Gera uma rede direcionada ou não direcionada.
- [`sara_weighted_network`](/scripts/sara_weighted_network.py) - Gera uma rede com peso nas arestas,
    direcionada ou não direcionada.

A rede gerada é salva no diretório `redes/`.

### Análise de Centralidade

O framework identifica os vértices de maior importância de acordo com as seguintes métricas de centralidade:

- Betweenness, PageRank, Degree, Curtidas, Retweets.

A detecção de centralidade é realizada por meio da utilização do script:

```
script/sara_centrality.py
```

O resultado deste script é salvo no diretório `resultados_importancia/`.

### Detecção de Comunidades

A detecção de comunidade neste framework é realizada por meio do módulo Overlap.

Esta ferramenta procura encontrar ego comunidades formada em torno de determinados usuários.

- Detecção de comunidades - Realiza a detecção de comunidades sobrepostas, utilize o resultado da centralidade ou outra sequência de importância para detecção de comunidades.

Modulo associado

- [`overlap.py`](/sara/detecta_comunidades)

### Análise de conteúdo

A análise de conteúdo presente nos tweets é realizada por meio de modelagem de tópicos,
distribuição inversa de frequência e nuvem de palavras.

Core:

- [`sara/core/topic_model`](/sara/core/topic_model.py)
- [`sara/core/tf_idf`](/sara/core/tf_idf.py)

Script:

- [`sara_content`](/sara/scripts/sara_content.py): Responsável pela geração da nuvem de palavras.

## Testes

Este projeto possui testes unitários implementados,
podendo ser executados com o seguinte comando:

``` console
python setup.py pytest
```

## Requerimentos

Testado em ambientes Ubuntu, CentOS 7

- Python versão 3.6, 3.7
- MongoDB
- [dependências](requirements.txt)

## Apoio

Este trabalho foi desenvolvido com apoio financeiro das seguintes agências de
fomento e universidade:

- Capes
- CNPq
- FAPEMIG
- UFSJ

## Artigos associados

Trabalhos relacionados a esta pesquisa que foram publicados em conferências:

- [SaraBotTagger - A Light Tool to Identify Bots in Twitter](https://link.springer.com/chapter/10.1007/978-3-030-65351-4_9)

- [A framework for the analysis of information propagation in social networks combining complex networks and text mining techniques full strip](https://dl.acm.org/doi/abs/10.1145/3323503.3360289)

- [Sara - A Semi-Automatic Framework for Social Network Analysis](https://sol.sbc.org.br/index.php/webmedia_estendido/article/view/8137/8012)
