# Guia de Instalação Sara

Este guia foi elaborado com o intuito de guiar a Instalação do Sara no ambiente ubuntu e sistemas operacionais ubuntu-like.

- Testado no ubuntu 18.04

## Resolução inicial de dependências

execute o script de instalação ou siga os passos a seguir:

- Script de instalação:
    > installSara.sh

- Atualize o seu sistema operacional:
    > sudo apt update
- Realize o upgrade do ambiente
    > sudo apt upgrade

- Instale o banco de dados, mongodb

    > https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

- Instale pip, virtualenv

    > sudo apt-get install build-essential libssl-dev libffi-dev python-dev

    > sudo apt install python3-pip

    > sudo apt install -y python3-venv

    > sudo pip install virtualenv

## Criando um ambiente virtual

Este ambiente funcionara como uma 'jaula', evitando conflito de dependências.

- Agora crie um ambiente dentro da pasta sara ou em uma pasta externa, todas as dependências especificas do projeto serão instalados nesse ambiente. Execute no terminal o comando abaixo:

> python3 -m venv saraEnv

- Agora ative este ambiente

> source saraEnv/bin/activate

Você visualizara uma tela similar a seguinte:

``` shell
(saraEnv)usuario:home/tutorial$:
```
**** obs ****: Observe que agora aparece no terminal o nome do ambiente ativado. Para desativar digite desactivate.

Pronto, agora você tem um ambiente virtual ativo. Agora instale todas as dependências do projeto disponíveis no requirements.txt. Com o terminal aberto execute:

> pip install -r requirements.txt

A tela do terminal devera estar similar a tela seguinte:

``` shell
(saraEnv)usuario:home/tutorial$ pip install -r requirements.txt
```


## Pós-Instalação
Caso tenha utilizado o script de instalação ative o ambiente virtual com o seguinte comando:

> source saraEnv/bin/activate

Agora digite no terminal, dentro do ambiente virtual:

> python3 -m spacy download pt_core_news_sm

execute o script nltk
 > python3 install_punkt_nltk.py

Pronto! Parabéns você instalou todas as dependências necessárias.

# Executando

Certifique-se de ter instalado o mongodb e coloque o mesmo para executar:

> sudo systemctl start mongod

Verifique se o mongo esta executando corretamente.

> sudo systemctl status mongod

## Atualize as Credências de desenvolvedor do Twitter.

Dentro da pasta sara_public/credencias altere o arquivo conexao_twitter.py


 ## Agora você pode executar coletas e análises rapidas com sara.

 ###  Coletando Tweets.

 Ative o ambiente virtual e digite:

 ``` shell
 (saraEnv)$: python sara_coletor.py <termo_a_ser_coletado> <limite_coleta> <colecao> <banco>
```

- termo_a_ser_coletado : Refente a hastag ou termo a ser monitorado.
- limite_coleta: referente ao número de tweets a ser coletado, para não estabelecer um limite digite 0
- colecao: A coleção onde os dados serão salvos no banco de dados.
- banco: O nome do banco onde os dados serão salvos.

### Gerando Núvem de palavras dos Tweets coletados(Conteúdo)

``` shell
(saraEnv)$: python sara_conteudo.py <banco> <colecao>
```

Caso ocorra algun erro , verifique se você executou o processo de pós-instalação.

No final do processo será gerada uma nuvem de palavras.

### Gerando Rede de Retweets(Estrutural)

``` shell
(saraEnv)$: python3 saraEstrutural.py <nome_rede> <nome_base> <nome_colecao> <True||False> <limite>
```
- nome_rede: Nome a ser utilizado para salvar a rede gerada.
- nome_base: Nome do banco de dados onde os tweets baixados estão presente.
- nome_colecao: Nome da coleção onde estão os dados.
- True ou False: Se true gera uma rede direcionada.
- limite: Número de tweets utilizados para geração da rede, para usar todos defina como 0.

A rede gerada sera salva na pasta redes, a ser gerada após a execução.
### Centralidade (Importância)

Para realização desta etapa é necessário que se tenha um grafo gerado.

Nesta etapa é gerada uma lista de nós ordernada por importância quanto a centralidade, que pode ser utilizada na detecção de comunidades.

``` shell
(saraEnv)$: python3 sara_centralidade.py <banco> <colecao> <grafo>
```

Entrada: grafo.gml

saída: Um ranking gravado na pasta resultados_importancia

### Sara Sentimento(Leia)

``` shell
(saraEnv)$: python3 sara_sentimento.py <banco> <colecao>
```

Nesta etapa é gerada um gráfico simples da análise de sentimento.


Pronto Fim do tutorial.
