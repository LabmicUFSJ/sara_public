"""
Verify if a account is bot.
This module is private.
"""
import json

import numpy as np
import pandas as pd
from joblib import load

from sara.core.config import sarabot_path
from sara.core.metadados import get_user_metadata
from sara.core.mongo.db import load_users
from sara.core.utils import create_path


def _save_list(path, data_list):
    print(f"File stored in {path}")
    with open(path, 'w') as arq:
        for data in data_list:
            arq.write(str(data['id'])+'\n')


class SaraBot:
    """SaraBotTagger Class."""
    # pylint:disable=too-many-instance-attributes
    def __init__(self, database, collection, limit=None):

        # Create a path
        self.path = f'{sarabot_path}{collection}/'
        create_path(self.path)
        self.human_list = []
        self.bot_list = []
        self.model = load('sara/core/bot_model/modelo_2.joblib')
        self.human_path = f'{self.path}human_result_{collection}.txt'
        self.bot_path = f'{self.path}bot_result_{collection}.txt'
        self.path_csv = f'{self.path}sarabot_result_{collection}.csv'
        self.metadata_csv = f'{self.path}sarabot_metadata_{collection}.csv'
        self.stats_path = f'{self.path}/stats_{collection}.json'
        self.database = database
        self.collection = collection
        self.limit = limit
        self.number_humans = 0
        self.number_bots = 0
        self.stats = []

    def _is_bot(self, user):
        """Check if user is a bot returning 1 or 0."""
        user_stats = get_user_metadata(user)
        user_table = pd.DataFrame([user_stats])
        user_table = user_table.drop(columns=['id_str'])
        user = np.array(user_table)
        return self.model.predict(user)[0]

    def run(self):
        """Check a number of accounts."""
        users = load_users(self.database, self.collection, self.limit)
        count = 0
        for user in users:
            print(f"checking {count}/{len(users)}")
            if self._is_bot(user):
                user['class'] = 'bot'
                self.bot_list.append(user)
            else:
                user['class'] = 'human'
                self.human_list.append(user)
            stats = get_user_metadata(user)
            stats.update({"class": user['class']})
            self.stats.append(stats)
            count += 1
        _save_list(self.bot_path, self.bot_list)
        _save_list(self.human_path, self.human_list)
        self.number_humans = len(self.human_list)
        self.number_bots = len(self.bot_list)
        return self.human_list, self.bot_list

    def get_stats_dict(self):
        """Return a dict with stats."""
        sum_users = self.number_bots+self.number_humans
        percent = (self.number_bots*100)/sum_users
        return {"humans": len(self.human_list), "bots": len(self.bot_list),
                "percent_bots": percent}

    # def save_csv(self):
    #     """Save data to csv."""
    #     data = self.human_list+self.bot_list
    #     table = pd.DataFrame(data)
    #     table.to_csv(self.path_csv, index="False")
    #     # save users metadata

    #     table = pd.DataFrame(self.stats)
    #     table.to_csv(self.metadata_csv, index="False")

    def save_json(self):
        """Save json."""
        stats = self.get_stats_dict()
        stats['colecao'] = self.collection

        with open(self.stats_path, 'w', encoding="utf8") as json_file:
            json.dump(stats, json_file)
class SaraBotStandalone:

    def __init__(self, model="sara/core/bot_model/modelo_2.joblib"):
        self.model = load(model)

    def is_bot(self, user_dict):
        user_stats = get_user_metadata(user_dict)
        user_table = pd.DataFrame([user_stats])
        user_table = user_table.drop(columns=['id_str'])
        user = np.array(user_table)
        return self.model.predict(user)[0]