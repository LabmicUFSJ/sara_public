# Guia de Instalação Sara

Este guia foi elaborado com o intuito de guiar a Instalação da Sara no ambiente Ubuntu e CentOS.

Testado em: 
 - Ubuntu 18.04
 - CentOS 7

## Instalação CentOs

- Instale o banco de dados, mongodb

    > https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

- Agora, execute o script de instalação:
    > installCentOs.sh

## Instalação Ubuntu

- Instale o banco de dados, mongodb

    > https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

Execute o script de instalação ou realize a instalação manual.

- Script de instalação:
    > installSara.sh

### Instalação Manual Ubuntu

- Atualize o seu sistema operacional:
    > sudo apt update

- Realize o upgrade do ambiente
    > sudo apt upgrade

- Instale pip, virtualenv

    > sudo apt-get install build-essential libssl-dev libffi-dev python-dev

    > sudo apt install python3-pip

    > sudo apt install -y python3-venv

    > sudo pip install virtualenv

### Criando um ambiente virtual

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


# Pós-Instalação
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


Pronto Fim do tutorial.
Para executar as suas primeiras análises consulte o guia de execução:
- [Guia de Execução](Guia_execucao.md)
