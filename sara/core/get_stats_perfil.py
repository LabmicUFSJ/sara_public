"""
Módulo de estatistica do usuario

Baseada na descrição:
https://github.com/cmagnobarbosa/spottingbot/blob/master/documentation/User.md

"""
import re
import datetime

# from pyxdameraulevenshtein import (
# normalized_damerau_levenshtein_distance as compara_nomes)


def check_name(name):
    """Verifica o nome"""
    numero_digitos = len(re.findall(r'[0-9]', name))
    return numero_digitos


def check_name_size(name):
    """Check size name"""
    size_name = len(name)
    return size_name


def check_description_length(description):
    """Check description length"""
    if description is None or str(type(description)) == str(type(0)):
        return 0.0
    try:
        size_description = len(description)
    except Exception as e:
        print(e, )
        print("Erro", description)
        exit()

    return size_description


def get_reputation(seguidores, seguindo):
    """calculate reputation of user"""
    try:
        return (seguidores / (seguidores + seguindo))
    except ZeroDivisionError:
        return 0.0


def prepara_nome(nome):
    """prepara string para comparacao."""
    return nome.replace(" ", "").replace("_", "").lower()


def check_year_account(year, data_coleta=None):
    """checa o ano da conta."""
    year = re.sub(r"[+].\d*", " ", year)
    year = year.replace("  ", "")
    date1 = datetime.datetime.strptime(year, '%a %b %d %H:%M:%S %Y')
    date1 = date1.strftime("%Y-%m-%d")
    if not data_coleta:
        date_today = datetime.datetime.now()
        date_today = date_today.strftime("%Y-%m-%d")
    else:
        date_today = data_coleta
    # to data
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date_today = datetime.datetime.strptime(date_today, "%Y-%m-%d")
    dif_data = abs(date1 - date_today).days
    return dif_data


def estatistica(user, data_coleta=None):
    """Recebe um dict user e retorna estatiscas sobre o perfil."""
    # pylint: disable=too-many-locals
    total_tweets = 0
    # carrega parametros iniciais
    name = prepara_nome(user.get("name"))

    # localização do perfil
    location = user.get('location')

    screen_name = prepara_nome(user.get("screen_name"))
    # descricao
    description = user.get('description')
    year = 0
    year = user.get('created_at')
    total_tweets = 0
    total_tweets = user.get('statuses_count')
    favourites_count = 0
    favourites_count = user.get('favourites_count')

    seguidores = 0
    seguindo = 0
    seguidores = user['followers_count']
    seguindo = user['friends_count']

    digitos_screen_name = 0
    # checa o número de digitos no screen_name
    digitos_screen_name = check_name(screen_name)
    # checa o número de digitos no nome
    digitos_name = check_name(name)

    # checa o tamanho do nome
    tam_name = check_name_size(name)
    # checa o tmanho do screen_name
    tam_screen_name = check_name_size(screen_name)
    # checa tamanho descrição
    tam_descricao = check_description_length(description)

    try:
        idade_conta = check_year_account(year, data_coleta)
    except Exception:
        pass
    # checa ano

    # tweets by day
    try:
        tweets_por_dia = total_tweets/idade_conta
        crescimento_seguidores = seguidores/idade_conta
        crescimento_favoritos = favourites_count/idade_conta
    except Exception:
        tweets_por_dia = total_tweets/1
        crescimento_seguidores = seguidores/1
        crescimento_favoritos = favourites_count/1

    relacao_seguidores_seguindo = get_reputation(seguidores, seguindo)

    try:
        year = year.split(" ")[-1]
    except Exception:
        pass

    metadado_usuario = {
        "id_str": user.get('id_str'),
        "ano_criacao": int(year),
        "total_tweets": total_tweets,
        "total_favoritos": favourites_count,
        "seguidores": seguidores,
        "seguindo": seguindo,
        "digitos_screen_name": digitos_screen_name,
        "digitos_nome": digitos_name,
        "tamanho_nome": tam_name,
        "tamanho_screen_name": tam_screen_name,
        "tamanho_descricao": tam_descricao,
        "idade_conta": idade_conta,
        "tweets_dia": tweets_por_dia,
        "crescimento_seguidores_dia": crescimento_seguidores,
        "crescimento_favoritos_dia": crescimento_favoritos,
        "location": location,
        "reputacao": relacao_seguidores_seguindo
    }

    return metadado_usuario
