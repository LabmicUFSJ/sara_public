"""
Sara
"""
import json
import sys
from pathlib import Path

import pandas as pd

from sara.core.mongo.db import get_client, load_database
from sara.core.sara_bot import SaraBotStandalone

BASE_URL = "https://twitter.com/intent/user"

try:
    database_name = sys.argv[1]
    collection_name = sys.argv[2]
    path_to_data = sys.argv[3]
except (KeyError, IndexError) as err_msg:
    print(f'Error {err_msg}')
    print(f"Digite python3 {sys.argv[0]} <database> "
          "<collection> <path_to_txt_with_names>")
    sys.exit(-1)


def save_json(stats_path, stats):
    """Save json."""
    with open(stats_path, 'w', encoding="utf8") as json_file:
        json.dump(stats, json_file)


def to_save(user, bot):
    """Return a JSON in formmat to save."""
    return {"screen_name": user['screen_name'], "id_str": user['id_str'],
            "bot": bot,
            'twitter_link': f"{BASE_URL}?user_id="+user['id_str']}


def load_ids(path_to_name):
    """Load data and return a list."""
    return [i.strip() for i in open(path_to_name, 'r')]


class SaraBotNames:
    """Find bots by Name"""

    def __init__(self):
        """Init the class."""
        self.bot_list = []
        self.human_list = []
        self.con = load_database(get_client(), database_name, collection_name)
        self.loaded_names = load_ids(path_to_data)
        self.sarabot = SaraBotStandalone()
        self.projection = {"user": 1, "retweeted.user": 1}

    def get_stats_dict(self):
        """Return a dict with stats."""
        number_bots = len(self.bot_list)
        number_humans = len(self.human_list)
        sum_users = number_bots+number_humans
        percent = (number_bots*100)/sum_users
        return {"humans": number_humans, "bots": number_bots,
                "percent_bots": percent}

    @staticmethod
    def check_saved(table_path):
        """Check if the save csv can be loaded."""
        table = pd.read_csv(table_path)
        print(f"Sized saved data {len(table)}")

    def main(self):
        """Main class."""

        for usr_name in self.loaded_names:
            find = self.con.find({"user.screen_name": usr_name},
                                 self.projection).limit(1)
            recovered = self.con.count_documents({'user.screen_name':
                                                  usr_name},
                                                 limit=1)
            if not recovered:
                find = self.con.find({"retweeted_status.user.screen_name":
                                      usr_name},
                                     self.projection).limit(1)
            for i in find:
                user = i.get('user') or i.get('retweeted_status.user')
                if self.sarabot.is_bot(user):
                    self.bot_list.append(to_save(user, 1))
                else:
                    self.human_list.append(to_save(user, 0))

        print(len(self.human_list), len(self.bot_list))
        base_path = Path(path_to_data)
        final = base_path.name.split("_")[1].replace('.txt', '')
        path_to_result = Path('resultados_bot', base_path.parent.parent.name,
                              final, base_path.parent.name)
        path_to_result.mkdir(parents=True, exist_ok=True)
        csv_name = base_path.name.replace('.txt', '.csv')
        bots_path = path_to_result.joinpath('bot_list_' + csv_name)
        humans_path = path_to_result.joinpath('human_list_' + csv_name)

        bots_table = pd.DataFrame(self.bot_list)
        humans_table = pd.DataFrame(self.human_list)

        humans_table.to_csv(humans_path, index=False)
        bots_table.to_csv(bots_path, index=False)
        # check if data can be loaded.
        self.check_saved(humans_path)
        if self.bot_list:
            self.check_saved(bots_path)
        print(f'Arquivos salvos em {bots_path}')
        print(f"Arquivos salvos em {humans_path}")
        print("OK")
        path_to_result = path_to_result.joinpath('stats_'+base_path.name)
        save_json(path_to_result, self.get_stats_dict())


main = SaraBotNames()
main.main()
