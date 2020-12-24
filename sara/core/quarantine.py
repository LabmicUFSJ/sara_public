"""
Quarantine
"""
import json

from sara.core.config import quarentine_path
from sara.core.utils import create_path
from sara.credenciais.conexao_twitter import inicia_conexao


class Quarantine:
    """Quarantine Class."""

    def __init__(self, users_list, subject):
        self.api = inicia_conexao()
        self.users_ids = users_list
        self.number_users = len(users_list)
        self.subject = subject
        self.path = f'{quarentine_path}{subject}'
        self.stats_path = f'{self.path}/stats_{subject}.json'
        self.suspended_path = f'{self.path}/deletados_{self.subject}.txt'
        create_path(self.path+"/")

    def run(self):
        """Check user_id."""
        users_temp = []
        requests = []
        users = []
        print(len(self.users_ids))
        for usr_id in self.users_ids:
            users_temp.append(usr_id)
            if len(users_temp) == 100:
                requests.append(users_temp)
                users_temp = []
        if len(users_temp) != 0:
            requests.append(users_temp)
        for request in requests:
            data_requested = self.api.UsersLookup(user_id=request,
                                                  return_json=True)
            users = users+data_requested
        users_exist = [user.get('id_str') for user in users]
        users_suspended = list(set(self.users_ids) - set(users_exist))
        print(f"Usuários verificados {self.number_users}")
        print("Usuários Deletados/suspensos: ", len(users_suspended))
        percent_suspended = (len(users_suspended)*100)/self.number_users
        print(f"Porcentagem de usuários suspensos {percent_suspended}")
        self.save_list(users_suspended)
        stats = {"Assunto": "Usuários marcados como Bot - Quarentena",
                 "Base": self.subject,
                 "Usuarios verificados": self.number_users,
                 "Usuarios Suspensos": len(users_suspended),
                 "Porcentagem Usuários suspensos": percent_suspended}
        self._save_json(stats)

    def _save_json(self, stats):
        """Save stats like JSON."""
        with open(self.stats_path, 'w', encoding='utf8') as json_file:
            json.dump(stats, json_file)

    def save_list(self, users_list):
        """Save list to file."""
        with open(self.suspended_path, 'w', encoding='utf8') as arq:
            for user in users_list:
                arq.write(str(user)+"\n")
