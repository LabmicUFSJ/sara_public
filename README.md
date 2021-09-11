# SARA

[![experimental](https://img.shields.io/badge/stability-experimental-red)](https://github.com/LabmicUFSJ/sara_public/) [![version](https://img.shields.io/badge/version-0.2-blue)](https://github.com/LabmicUFSJ/sara_public/blob/master/CHANGELOG.md) [![labmic](https://img.shields.io/badge/UFSJ-Labmic-lightgrey)](https://ufsj.edu.br/)
[![Build Python Package](https://github.com/LabmicUFSJ/sara/actions/workflows/main.yml/badge.svg)](https://github.com/LabmicUFSJ/sara/actions/workflows/main.yml)
[![Tests and Linter](https://github.com/LabmicUFSJ/sara/actions/workflows/python-package.yml/badge.svg)](https://github.com/LabmicUFSJ/sara/actions/workflows/python-package.yml)
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow)](https://github.com/LabmicUFSJ/sara/actions/workflows/python-package.yml)

A SARA é um framework semi-automatizado para coleta e análise de dados de
redes sociais online (RSO), utilizando redes complexas, aprendizagem de máquina
e mineração de texto.

Desenvolvido no Laboratório de Modelagem Computacional e Inteligência Computacional (LABMIC) da Universidade Federal de São João del-Rei (UFSJ)

Estado : Em desenvolvimento / Experimental

Site : https://labmicufsj.github.io/sara_public/

SaraBotTagger Web Tool - https://sara-labmic.herokuapp.com/

SaraDashboard - https://sara-dash.herokuapp.com/

SaraGraphVisualizer  - https://saragraph.herokuapp.com/

## Guias

- [Guia geral como utilizar.](sara/guides/Guia_execucao.md)
- [Agendamento de Coleta.](sara/guides/Guia_agendamento.md)

## Instalação

Crie um ambiente virtual com o comando a seguir:

``` console
python3.7 -m venv <nome_ambiente>
```

Agora ative o ambiente virtual

``` console
source <nome_ambiente>/bin/activate
```

Após a criação e ativação do ambient execute:

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

Scripts associados:

- [`sara_stream`](scripts/sara_stream.py) - Realiza as coletas de tweets em tempo real.
- [`sara_scheduled_stream`](scripts/sara_scheduled_stream.py) - Realiza coletas de acordo com agendamento.
- [`credentials/twitter_api`](sara/credentials/twitter_api.py) - Contém os dados de acesso da API do Twitter.

Core:

- [`sara/core/collector.py`](sara/core/collector.py)

Os dados coletados são salvos em um banco de dados não relacional (MongoDB).

### Geração da Rede

A geração da rede é realizada utilizando o módulo `network_generators`.

Scripts:

- [`sara_network`](/scripts/sara_network.py) - Gera uma rede direcionada ou não direcionada.
- [`sara_weighted_network`](/scripts/sara_weighted_network.py) - Gera uma rede com peso nas arestas,
    direcionada ou não direcionada.

A rede gerada é salva no diretório `redes/`.

Core:

- [`sara/core/network_generators`](sara/core/network_generators)

### Análise de Centralidade

O framework identifica os vértices de maior importância de acordo com as seguintes métricas de centralidade:

- Betweenness, PageRank, Degree, Curtidas, Retweets.

A detecção de centralidade é realizada por meio da utilização do script:

Script:

- [`script/sara_centrality.py`](script/sara_centrality.py)

Core:

- [`sara/core/centrality`](sara/core/centrality)
   
O resultado deste script é salvo no diretório `resultados_importancia/`.

### Detecção de Comunidades

A detecção de comunidades neste framework é realizada utilizando o módulo de overlap e o algoritmo de Louvain.

Esta ferramenta procura encontrar ego-comunidades formada em torno de determinados usuários.

- Detecção de comunidades sobrepostas - Utilize o resultado da centralidade ou outra sequência de importância para detecção de comunidades.

Modulo associado

- [`overlap.py`](/sara/utils/community_overlap_detection)

### Análise de conteúdo

A análise de conteúdo presente nos tweets é realizada por meio de modelagem de tópicos,
distribuição inversa de frequência e nuvem de palavras.

Script:

- [`sara_content`](/sara/scripts/sara_content.py): Responsável pela geração da nuvem de palavras.

Core:

- [`sara/core/topic_model`](/sara/core/topic_model.py)
- [`sara/core/tf_idf`](/sara/core/tf_idf.py)

## Detecção de contas automatizadas
 
 - SaraBotTagger

## Testes

Este projeto possui testes unitários implementados,
podendo ser executados com o seguinte comando:

``` console
python setup.py pytest
```

## Requerimentos

Testado em ambientes Ubuntu, CentOS 7

- Python versão 3.6, 3.7, 3.8, 3.9
- [MongoDB](https://www.mongodb.com/try/download/community)
- [dependências](requirements.txt)

## Apoio

Este trabalho foi desenvolvido com apoio financeiro das seguintes agências de
fomento e universidade:

- Capes
- CNPq
- FAPEMIG
- UFSJ

## Orientador
- Orientador: Vinícius da Fonseca Vieira

## Agradecimentos e Pesquisadores envolvidos
- Carolina Ribeiro Xavier
- Lucas Félix
- Antônio Pedro Santos Alves

## Artigos associados

Trabalhos relacionados a esta pesquisa que foram publicados em conferências:

- [SaraBotTagger - A Light Tool to Identify Bots in Twitter](https://link.springer.com/chapter/10.1007/978-3-030-65351-4_9)

- [A framework for the analysis of information propagation in social networks combining complex networks and text mining techniques full strip](https://dl.acm.org/doi/abs/10.1145/3323503.3360289)

- [Sara - A Semi-Automatic Framework for Social Network Analysis](https://sol.sbc.org.br/index.php/webmedia_estendido/article/view/8137/8012)
