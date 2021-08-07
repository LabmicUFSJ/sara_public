"""SARA quarantine.

Atention: This module will be replaced by is_online script.

"""
import sys

from sara.core.quarantine import Quarantine

try:
    name_file = sys.argv[0]
    list_users = sys.argv[1]
    subject = sys.argv[2]
except IndexError as exc:
    print(f"erro {exc}")
    print(f"Enter: python {name_file} <list_of_users> <subject>")
    sys.exit()

with open(list_users, 'r') as arq:
    users_ids = [user_id.strip() for user_id in arq]

quarantine = Quarantine(users_ids, subject)
quarantine.run()
