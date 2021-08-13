"""
Gera metados do usuário.
Generate user metadata.

"""
import json
import datetime
import re
from unicodedata import normalize


def _remove_special_characters(text):
    """Remove special characters."""
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def _get_ratio(user_a, user_b):
    """Get ratio."""
    user_b = 1 if int(user_b) == 0 else user_b
    user_a = 1 if int(user_b) == 0 else user_a
    return user_a/user_b


def _count_numbers(text):
    """Count numbers in text."""
    return len(re.findall(r'[0-9]', text))


def _has(text, term):
    """Verify if text contains term."""
    text = _remove_special_characters(text.lower())
    return 1 if term in text.split(" ") else 0


def _get_reputation(followers, following):
    """Get reputation of user."""
    try:
        return followers / (followers + following)
    except ZeroDivisionError:
        return 0.0


def _pre_processing(name):
    """Remove space and _ and transforme name to lower."""
    return name.replace(" ", "").replace("_", "").lower()


def _get_account_age(year, collect_date=None):
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


def get_user_from_dict(user, data_coleta=None):
    """Return user metadata."""
    # pylint: disable=too-many-locals
    # remove space and _ from name and screen_name
    name = _pre_processing(user.get('name'))
    screen_name = _pre_processing(user.get("screen_name"))

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
    screen_name_digits = _count_numbers(screen_name)
    name_digits = _count_numbers(name)

    # checa o tamanho do nome.
    name_size = len(name)
    # checa o tmanho do screen_name.
    screen_name_size = len(screen_name)

    try:
        account_age = _get_account_age(year, data_coleta)
    except TypeError as error:
        print(f"Error in get account age: {error}")
        return None

    # tweets by day
    temp_age = 1 if account_age == 0 else account_age
    tweets_by_day = tweets_count/temp_age
    followers_growth = followers/temp_age
    fav_growth = favourites_count/temp_age

    # seguindo/seguidores
    ratio_following_followers = _get_ratio(following, followers)

    # Fav/seguindo
    fav_following = _get_ratio(favourites_count, following)

    # Fav/Seguidores
    fav_followers = _get_ratio(favourites_count, followers)

    # seguidores/(seguidores+seguindo)
    reputation = _get_reputation(followers, following)

    # crescimento amigos , seguindo/idade da conta.
    # following increment by day.
    following_growth = _get_ratio(following, account_age)

    # has bot in description.
    analise_bot_descricao = 0
    analise_bot_descricao = _has(description, 'bot')
    analise_bot_descricao = _has(description, 'robo')

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
    return UserMetadata(user_metadata)


class UserMetadata:
    """User metadata class."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, user_dict):
        """ Receive as argument a dictionary with user metadata."""
        self.id_str = user_dict['id_str']
        self.conta_verificada = user_dict['conta_verificada']
        self.imagem_padrao = user_dict['imagem_padrao']
        self.imagem_background = user_dict['imagem_background']
        self.perfil_padrao = user_dict['perfil_padrao']
        self.seguidores = user_dict['seguidores']
        self.seguindo = user_dict['seguindo']
        self.total_favoritos = user_dict['total_favoritos']
        self.total_tweets = user_dict['total_tweets']
        self.idade_conta = user_dict['idade_conta']
        # relacao_seguindo_seguidores
        rel_seguindo_seguidores = user_dict['relacao_seguindo_seguidores']
        self.relacao_seguindo_seguidores = rel_seguindo_seguidores
        self.reputacao = user_dict['reputacao']
        self.fav_seguindo = user_dict['fav_seguindo']
        self.fav_seguidores = user_dict['fav_seguidores']
        self.analise_bot_descricao = user_dict['analise_bot_descricao']
        self.tamanho_screen_name = user_dict['tamanho_screen_name']
        self.tamanho_nome = user_dict['tamanho_nome']
        self.tamanho_descricao = user_dict['tamanho_descricao']
        self.crescimento_amigos = user_dict['crescimento_amigos']
        crescimento_seguidores = user_dict['crescimento_seguidores_dia']
        self.crescimento_seguidores_dia = crescimento_seguidores
        self.tweets_dia = user_dict['tweets_dia']
        self.digitos_screen_name = user_dict['digitos_screen_name']
        self.digitos_nome = user_dict['digitos_nome']
        self.ano_criacao = user_dict['ano_criacao']
        self.crescimento_favoritos_dia = user_dict['crescimento_favoritos_dia']

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError(f'Error comparing Users Metadada:{other} is not'
                             f'an instance of {self.__class__}')
        return self.as_dict() == other.as_dict()

    def as_dict(self):
        """Return an UserMetadata dictionary.

            This dictionary can be used on SaraBotTagger.
        """

        user_metadata = {
            "id_str": self.id_str,
            "conta_verificada": self.conta_verificada,
            "imagem_padrao": self.imagem_padrao,
            "imagem_background": self.imagem_background,
            "perfil_padrao": self.perfil_padrao,
            "seguidores": self.seguidores,
            "seguindo": self.seguindo,
            "total_favoritos": self.total_favoritos,
            "total_tweets": self.total_tweets,
            "idade_conta": self.idade_conta,
            "relacao_seguindo_seguidores": self.relacao_seguindo_seguidores,
            "reputacao": self.reputacao,
            "fav_seguindo": self.fav_seguindo,
            "fav_seguidores": self.fav_seguidores,
            "analise_bot_descricao": self.analise_bot_descricao,
            "tamanho_screen_name": self.tamanho_screen_name,
            "tamanho_nome": self.tamanho_nome,
            "tamanho_descricao": self.tamanho_descricao,
            "crescimento_amigos": self.crescimento_amigos,
            "crescimento_seguidores_dia": self.crescimento_seguidores_dia,
            "tweets_dia": self.tweets_dia,
            "digitos_screen_name": self.digitos_screen_name,
            "digitos_nome": self.digitos_nome,
            "ano_criacao": self.ano_criacao,
            "crescimento_favoritos_dia": self.crescimento_favoritos_dia
            }
        return user_metadata

    def as_json(self):
        """Return the UserMetadata like a JSON."""
        return json.dumps(self.as_dict())
