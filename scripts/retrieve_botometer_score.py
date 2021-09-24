"""
Get Botometer score.

This script uses Botometer API.
"""
import sys
from random import sample

from sara.core.botometer_api import check_users_botometer
from sara.core.collector import get_users_by_id
from sara.core.sara_data import SaraData
from sara.core.utils import load_txt

try:
    path_to_file = sys.argv[1]
    database_name = sys.argv[2]
    collection_name = sys.argv[3]
except IndexError as error:
    print(f"Error {error}")
    print(f"Please, input python {sys.argv[0]} <path_to_file> <database> "
          " <collection>")
    sys.exit(-1)


def split_list(data, size):
    """split the list the elements."""
    for i in range(0, len(data), size):
        yield data[i:i+size]


def is_online(users):
    """Check if a user is online"""
    users_online = []
    for ids in split_list(users, 100):
        for result in get_users_by_id(ids):
            users_online.append(result.get('id_str'))
    return users_online


def main(users):
    """Get Botometer score and save in database."""
    users_online = is_online(users)
    print(f"Number of users online: {len(users_online)}")
    result = check_users_botometer(users_online)
    data = SaraData(database=database_name, collection_name=collection_name)
    for tdata in result:
        data.save_data(result[tdata])
    print("All data saved in mongoDB")


if __name__ == '__main__':
    user_ids = load_txt(path_to_file)
    selected_users = sample(user_ids, 1500)
    main(selected_users)
