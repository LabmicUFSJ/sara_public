"""
Módulo de coleta web.

* Necessita de atualização
"""
import time

# pylint: disable= import-error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.keys import Keys

# default template google chrome
# profile = "/home/carlospc/.config/google-chrome"
options = Options()
options.headless = False
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
# options.add_argument("user-data-dir="+profile)
# driver=webdriver.Chrome(options=options)
# drive.get("https://www.google.com.br")

# path twitter
# https://twitter.com/shannongsims/status/1112466606922317827
# https://twitter.com/{username}/status/{status_id}

LINK_DEFAULT = "https://twitter.com/"


def scrool(driver):
    """Realiza o scrool pela pagina."""
    element2 = driver.find_element_by_css_selector("div.stream-footer")
    driver.execute_script("arguments[0].scrollIntoView(false)", element2)


def save_data(name, data):
    """save data to file json"""
    arq = open(name + ".txt", "a")
    arq.write(str(data))
    arq.write("\n")
    arq.close()


def get_comments(dados, username, status_id, msg_set):
    "get comments"
    # msg_set=set()
    soup = BeautifulSoup(dados, "html.parser")
    # replies_content=soup.select("div.replies-to.permalink-inner.permalink-replies")
    # usr=soup.select("spam.username.u-dir.u-textTruncate")
    comments = soup.select("p.TweetTextSize.js-tweet-text.tweet-text")
    for i in comments:
        msg = str(
            {"usr_source": username, "status_id": status_id, "comment": i.text}
        )
        msg_set.add(msg)
        if msg not in msg_set:
            print("tweet", msg)
    return msg_set


def get_data(username, status_id, nome_arquivo="last_comentarios.txt"):
    """get data """
    driver = webdriver.Chrome(options=options)
    link_path = f"https://twitter.com/{username}/status/{status_id}"
    driver.get(link_path)
    print(f"Coletando comentários de {link_path}")
    controle_coletados = set()
    out_flag = 2
    last = 0
    while True:
        element2 = driver.find_element_by_css_selector("div.stream-footer")
        driver.execute_script("arguments[0].scrollIntoView(false)", element2)
        time.sleep(2)
        content = driver.page_source
        controle_coletados = get_comments(
            content, username, status_id, controle_coletados
        )
        # controla o numero de scrolls na pagina
        print(f"num comentarios coletados:{len(controle_coletados)}")
        if len(controle_coletados) != last:
            last = len(controle_coletados)
        else:
            out_flag -= 1
            print(f"repetido.. restam {out_flag} repeticoes")
        if out_flag <= 0:
            break
    for i in controle_coletados:
        save_data(nome_arquivo, i)
    print(f"Os dados foram salvos em {nome_arquivo}")
    driver.close()


# get_data("partidonovo30","1121878251067060224")
# lista=['1098386646784008192', '1098591862020026369', '1096504360060796928',
# '1098980628815642624', '1098274572409946115', '1098600204780138502',
# '1100109532108328960', '1098577431294894082', '1098609392424009729',
# '1097852181104021505', '1097852505629904898', '1098610088934293504',
# '1095064142506020866', '1098388437596626945']

# lista=['1098959262791991301', '1098618253608407040', '1092716603127533568',
# '1098248521386475520', '1098253247754702848', '1099048420789112833',
# '1098705684282204161', '1100082941777055745', '1099644956107517954',
# '1096381284958552064', '1097531260912787456', '1094720494836871175',
# '1099357528826281986', '1100733281056813056', '1100063407745716224',
# '1100738842372571136']


# for i in lista:
#     get_data("GuilhermeBoulos",i)
# div.permalink.light-inline-actions.stream-uncapped.has-replies.original-permalink-page

# driver.close()
