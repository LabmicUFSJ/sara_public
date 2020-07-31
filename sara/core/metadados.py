"""
Gera metados do usuário.
Generate user metadata.

Obs: This module is private.
"""
import re
import datetime
from unicodedata import normalize


def _remove_special_characters(text):
    """Remove special characters."""
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def get_ratio(a, b):
    """Get ratio."""
    b = 1 if int(b) == 0 else b
    a = 1 if int(b) == 0 else a
    return a/b


def count_numbers(text):
    """Count numbers in text."""
    return len(re.findall(r'[0-9]', text))


def has(text, term):
    """Verify if text contains term."""
    text = _remove_special_characters(text.lower())
    return 1 if term in text.split(" ") else 0


def get_reputation(followers, following):
    """Get reputation of user."""
    try:
        return (followers / (followers + following))
    except ZeroDivisionError:
        return 0.0


def pre_processing(name):
    """Remove space and _ and transforme name to lower."""
    return name.replace(" ", "").replace("_", "").lower()


def get_account_age(year, collect_date=None):
    """
    Return account age in days.
    * Need Refactor
    """
    year = re.sub(r"[+].\d*", " ", year)
    year = year.replace("  ", "")
    date1 = datetime.datetime.strptime(year, '%a %b %d %H:%M:%S %Y')
    date1 = date1.strftime("%Y-%m-%d")
    if not collect_date:
        date_today = datetime.datetime.now()
        date_today = date_today.strftime("%Y-%m-%d")
    else:
        date_today = collect_date
    # to data
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
    date_today = datetime.datetime.strptime(date_today, "%Y-%m-%d")
    diff_data = abs(date1 - date_today).days
    return diff_data


def get_user_metadata(user, data_coleta=None):
    """Return user metadata."""
    # pylint: disable=too-many-locals

    # remove space and _ from name and screen_name
    name = pre_processing(user.get('name'))
    screen_name = pre_processing(user.get("screen_name"))

    background_image = 1 if user.get('profile_use_background_image') else 0

    # imagem padrão, binary attribute
    default_image = 1 if user.get('default_profile_image') else 0

    # perfil padrao, default profile
    default_profile = 1 if user.get('default_profile') else 0

    # localização do perfil
    # location = user.get('location')

    # get user description
    description = user.get('description', ' ')
    description = ' ' if description is None else description
    description_size = len(description)

    # checa tamanho descrição.

    if 'user_created_at' in user:
        year = user.get('user_created_at')
    else:
        year = user.get('created_at')

    # Total tweets, Número total de tweets postado pelo usuário.
    # Number of tweets posted by the user.
    tweets_count = user.get('statuses_count', 0)

    # Curtidas.
    favourites_count = user.get('favourites_count', 0)

    # seguidores.
    # User A is followed by user B.
    followers = user.get('followers_count', 0)

    # seguindo
    # User A is following B
    following = user.get('friends_count', 0)

    # Checa o número de digitos no screen_name, name.
    # Count digits in name and screen_name.
    screen_name_digits = count_numbers(screen_name)
    name_digits = count_numbers(name)

    # checa o tamanho do nome.
    name_size = len(name)
    # checa o tmanho do screen_name.
    screen_name_size = len(screen_name)

    try:
        account_age = get_account_age(year, data_coleta)
    except Exception as e:
        print(e)
        return

    # tweets by day
    temp_age = 1 if account_age == 0 else account_age
    tweets_by_day = tweets_count/temp_age
    followers_growth = followers/temp_age
    fav_growth = favourites_count/temp_age

    # seguindo/seguidores
    ratio_following_followers = get_ratio(following, followers)

    # Fav/seguindo
    fav_following = get_ratio(favourites_count, following)

    # Fav/Seguidores
    fav_followers = get_ratio(favourites_count, followers)

    # seguidores/(seguidores+seguindo)
    reputation = get_reputation(followers, following)

    # crescimento amigos , seguindo/idade da conta.
    # following increment by day.
    following_growth = get_ratio(following, account_age)

    # has bot in description.
    analise_bot_descricao = 0
    analise_bot_descricao = has(description, 'bot')
    analise_bot_descricao = has(description, 'robo')

    # checa_nome, Verify if name contains bot. Binary.
    # analise_bot_nome = has(name, 'bot')
    # analise_bot_nome = has(name, 'robo')

    # conta verificada, verify if account has been verified.
    verified = 1 if user.get('verified') else 0

    year = int(year.split(" ")[-1])
    # id_str = user.get('user_id') or user.get('id_str')
    try:
        user_id = user['id']
    except KeyError:
        user_id = user['user_id']

    user_metadata = {
        "id_str": str(user_id),
        "conta_verificada": verified,
        "imagem_padrao": default_image,
        "imagem_background": background_image,
        "perfil_padrao": default_profile,
        "seguidores": followers,
        "seguindo": following,
        "total_favoritos": favourites_count,
        "total_tweets": tweets_count,
        "idade_conta": account_age,
        "relacao_seguindo_seguidores": ratio_following_followers,
        "reputacao": reputation,
        "fav_seguindo": fav_following,
        "fav_seguidores": fav_followers,
        "analise_bot_descricao": analise_bot_descricao,
        "tamanho_screen_name": screen_name_size,
        "tamanho_nome": name_size,
        "tamanho_descricao": description_size,
        "crescimento_amigos": following_growth,
        "crescimento_seguidores_dia": followers_growth,
        "tweets_dia": tweets_by_day,
        "digitos_screen_name": screen_name_digits,
        "digitos_nome": name_digits,
        "ano_criacao": year,
        "crescimento_favoritos_dia": fav_growth
    }

    return user_metadata
