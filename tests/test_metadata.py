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
            "friends_count": 100,
        }

        self.expected = {
            "id_str": "258764",
            "conta_verificada": 0,
            "imagem_padrao": 0,
            "imagem_background": 0,
            "perfil_padrao": 1,
            "seguidores": 20,
            "seguindo": 100,
            "total_favoritos": 10,
            "total_tweets": 300,
            "idade_conta": 407,
            "relacao_seguindo_seguidores": 5.0,
            "reputacao": 0.16666666666666666,
            "fav_seguindo": 0.1,
            "fav_seguidores": 0.5,
            "analise_bot_descricao": 0,
            "tamanho_screen_name": 7,
            "tamanho_nome": 8,
            "tamanho_descricao": 13,
            "crescimento_amigos": 0.2457002457002457,
            "crescimento_seguidores_dia": 0.04914004914004914,
            "tweets_dia": 0.7371007371007371,
            "digitos_screen_name": 0,
            "digitos_nome": 0,
            "ano_criacao": 2020,
            "crescimento_favoritos_dia": 0.02457002457002457,
        }

    @patch('sara.core.metadata.UserMetadata')
    def test_get_user_from_dict(self, mock_metadata):
        """Test get get_user_from_dict"""
        get_user_from_dict(self.user_dict)
        self.assertEqual(mock_metadata.call_count, 1)

    def test_as_dict(self):
        """Test as_dict method."""
        response = get_user_from_dict(self.user_dict, '2021-08-8')
        self.assertEqual(response.as_dict(), self.expected)

    def test_as_json(self):
        """Test as_json method."""
        response = get_user_from_dict(self.user_dict, '2021-08-8')
        self.assertEqual(json.loads(response.as_json()), self.expected)
