"""
Metadata tests
"""
import json
from unittest import TestCase
from unittest.mock import patch

from sara.core.metadata import get_user_from_dict


class TestSaraMetadata(TestCase):
    """Test SaraData class."""

    def setUp(self):
        """Startup method."""
        self.user_dict = {
                        "id": "258764",
                        "name": "mock_user",
                        "screen_name": "user_one",
                        "profile_use_background_image": False,
                        "default_profile_image": "",
                        "default_profile": True,
                        "description": "ordinary user",
                        "user_created_at": "Sat Jun 27 00:37:29 +0000 2020",
                        "statuses_count": 300,
                        "favourites_count": 10,
                        "followers_count": 20,
                        "friends_count": 100
                        }

    @patch('sara.core.metadata.UserMetadata')
    def test_get_user_from_dict(self, mock_metadata):
        """Test get get_user_from_dict"""
        get_user_from_dict(self.user_dict)
        self.assertEqual(mock_metadata.call_count, 1)

    def test_as_dict(self):
        """Test as_dict method."""
        expected = {
                    'analise_bot_descricao': 0,
                    'ano_criacao': 2020,
                    'conta_verificada': 0,
                    'crescimento_amigos': 0.24271844660194175,
                    'crescimento_favoritos_dia': 0.024271844660194174,
                    'crescimento_seguidores_dia': 0.04854368932038835,
                    'digitos_nome': 0,
                    'digitos_screen_name': 0,
                    'fav_seguidores': 0.5,
                    'fav_seguindo': 0.1,
                    'id_str': '258764',
                    'idade_conta': 412,
                    'imagem_background': 0,
                    'imagem_padrao': 0,
                    'perfil_padrao': 1,
                    'relacao_seguindo_seguidores': 5.0,
                    'reputacao': 0.16666666666666666,
                    'seguidores': 20,
                    'seguindo': 100,
                    'tamanho_descricao': 13,
                    'tamanho_nome': 8,
                    'tamanho_screen_name': 7,
                    'total_favoritos': 10,
                    'total_tweets': 300,
                    'tweets_dia': 0.7281553398058253
                }

        response = get_user_from_dict(self.user_dict)
        self.assertEqual(response.as_dict(), expected)

    def test_as_json(self):
        """Test as_json method."""
        expected = {
            'analise_bot_descricao': 0,
            'ano_criacao': 2020,
            'conta_verificada': 0,
            'crescimento_amigos': 0.24271844660194175,
            'crescimento_favoritos_dia': 0.024271844660194174,
            'crescimento_seguidores_dia': 0.04854368932038835,
            'digitos_nome': 0,
            'digitos_screen_name': 0,
            'fav_seguidores': 0.5,
            'fav_seguindo': 0.1,
            'id_str': '258764',
            'idade_conta': 412,
            'imagem_background': 0,
            'imagem_padrao': 0,
            'perfil_padrao': 1,
            'relacao_seguindo_seguidores': 5.0,
            'reputacao': 0.16666666666666666,
            'seguidores': 20,
            'seguindo': 100,
            'tamanho_descricao': 13,
            'tamanho_nome': 8,
            'tamanho_screen_name': 7,
            'total_favoritos': 10,
            'total_tweets': 300,
            'tweets_dia': 0.7281553398058253
        }
        response = get_user_from_dict(self.user_dict)
        self.assertEqual(json.loads(response.as_json()), expected)
