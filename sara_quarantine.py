import sys
from sara.core.quarantine import Quarantine


try:
    name_file = sys.argv[0]
    list_users = sys.argv[1]
    subject = sys.argv[2]
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Digite {name_file} <nome_lista_usuarios> <assunto_analisado>")
    sys.exit()

with open(list_users, 'r') as arq:
    users_ids = [user_id.strip() for user_id in arq]

quarantine = Quarantine(users_ids, subject)
quarantine.run()
