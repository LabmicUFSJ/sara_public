"""
Main coletor web.
* necessita de atualização
"""

import datetime

# p.TweetTextSize.js-tweet-text.tweet-text
import sys
import time

import coletor_web.coletor_comentarios as coletor
from bs4 import BeautifulSoup

# import conexao_twitter as conexao
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.keys import Keys


def generate_interval(inicio, final):
    """Gera um intervalo de data."""
    if "/" in inicio:
        pattern = "/"
    elif "-" in inicio:
        pattern = "-"
    ano, mes, dia = inicio.split(pattern)
    ano_f, mes_f, dia_f = final.split(pattern)
    start = datetime.datetime(int(ano), int(mes), int(dia), 0, 0, 0)
    end = datetime.datetime(int(ano_f), int(mes_f), int(dia_f), 0, 0, 0)
    delta = end - start
    datas = []
    for i in range(delta.days + 1):
        data = start + datetime.timedelta(days=i)
        datas.append(str(data).split(" ")[0])
    return datas


def save_data(name, data):
    """save data to file json"""
    arq = open(name + ".txt", "a")
    arq.write(str(data))
    arq.write("\n")
    arq.close()


def save_set(name, msg, dia):
    """save data."""
    arq = open(name + "_global.txt", "a")
    mensagem = {"dia": dia, "msg": msg}
    arq.write(str(mensagem))
    arq.write("\n")
    arq.close()


def load_dataset():
    """load dataset."""
    lista = []
    arq = open("sementes", "r")
    for i in arq:
        lista.append(i.strip())
    return lista


# def open_sementes()
# default template google chrome
# profile="/home/carlospc/.config/google-chrome"
options = Options()
options.headless = False
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
# options.add_argument("user-data-dir="+profile)


# usernames=load_dataset()


def coletor_global():
    """Coletor global de replies."""
    days = generate_interval("2019-01-01", "2019-02-01")
    name_file = "previdencia_janeiro"
    controle_tempo = 1
    for day in days:
        if controle_tempo >= len(days):
            break
        final = days[controle_tempo]
        default = "https://twitter.com/search?l=&q=previdencia%20since%3A"
        link_term2 = default + f"{day}%20until%3A{final}&src=typd&lang=pt"
        controle_tempo += 1
        # link_path=f"https://twitter.com/{username}/status/{status_id}"
        driver = webdriver.Chrome(options=options)
        driver.get(link_term2)
        ant = 0
        lista_tweets = set()
        limiar_repeticao = 0
        print(f"Coletando Tweets do dia {day} final {final}")
        while True:
            try:
                element2 = driver.find_element_by_css_selector(
                    "div.stream-footer"
                )
            except Exception as exc:
                print(f"Usuário sem twitter... {exc}")
                break
            driver.execute_script(
                "arguments[0].scrollIntoView(false)", element2
            )
            time.sleep(2)
            element = driver.find_elements_by_css_selector(
                "p.TweetTextSize.js-tweet-text.tweet-text"
            )
            for i in element:
                # print(i.get_attribute("innerHTML"))
                content = i.get_attribute("innerHTML")
                mensagem = BeautifulSoup(content, "html.parser")
                msg = mensagem.get_text()
                msg = msg.replace("\n", "")
                # mensagem_dic={"msg":msg}
                if msg not in lista_tweets:
                    lista_tweets.add(msg)
                    save_set(name_file, msg, day)
            print("Tweets coletados", len(lista_tweets))
            if ant != len(lista_tweets):
                ant = len(lista_tweets)
            else:
                print("repeticão....")
                limiar_repeticao += 1
            if limiar_repeticao >= 2:
                break

        driver.close()


def coletor_especifico(usernames):
    """Coletor especifico."""
    cont_username = 0
    for username in usernames:
        print(
            f"Coletando o usuário: {username}"
            f" Progresso {cont_username}/{len(usernames)}"
        )
        cont_username += 1
        default = "https//twitter.com/"
        link_term = default + f"search?l=&q=from%3A{username}&src=typd&lang=pt"
        # link_term=f"https://twitter.com/search?q=%20from%3A{username}
        # %20since%3A2019-05-08%20until%3A2019-05-08&src=typd"

        # link_path=f"https://twitter.com/{username}/status/{status_id}"
        driver = webdriver.Chrome(options=options)
        driver.get(link_term)
        elements = driver.find_elements_by_css_selector("div.stream")
        status_list = []
        for element in elements:
            msg = element.get_attribute("innerHTML")
            soup = BeautifulSoup(msg, "html.parser")
            links = soup.select(
                "a.tweet-timestamp.js-permalink.js-nav.js-tooltip"
            )

            for link in links:
                dados = link['href'].split("/")
                status_list.append(dados[3])
                print(f"Mapeando o link:{link['href']}")
                try:
                    coletor.get_data(dados[1], dados[3])
                except Exception as exc:
                    print(f"erro {exc}")
                    sys.exit()
        cont = 0
        while cont < 100:
            try:
                element2 = driver.find_element_by_css_selector(
                    "div.stream-footer"
                )
            except Exception:
                # out=True
                break
            driver.execute_script(
                "arguments[0].scrollIntoView(false)", element2
            )
            time.sleep(2)
            cont += 1
        # if(out is True):
        #     out=False
        #     break
        content = driver.execute_script(
            "return arguments[0].innerHTML;", elements
        )
        elements = driver.find_elements_by_css_selector(
            "p.TweetTextSize.js-tweet-text.tweet-text"
        )
        cont = 0
        print("Tamanho ", len(elements))
        for element in elements:
            # print(i.get_attribute("innerHTML"))
            content = element.get_attribute("innerHTML")
            mensagem = BeautifulSoup(content, "html.parser")
            msg = mensagem.get_text()
            msg = msg.replace("\n", "")
            try:
                mensagem_dic = {
                    "status_id": status_list[cont],
                    "username": username,
                    "msg": msg,
                }
            except Exception as exc:
                print(f"error {exc}")
                mensagem_dic = {
                    "status_id": "",
                    "username": username,
                    "msg": msg,
                }
            save_data("previdencia_lista", mensagem_dic)
            cont += 1

        driver.close()


# coletor_global()
lista = []
tweet_ids = open("sementes", "r")
for id_tweet in tweet_ids:
    lista.append(id_tweet.strip())
coletor_especifico(lista)
