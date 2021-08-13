"""
SaraBotTagger core

This module is still under development.
"""
import json
import os

import numpy as np
import pandas as pd
from joblib import load

from sara.core.config import sarabottagger_path
from sara.core.metadata import get_user_from_dict
from sara.core.mongo.db import load_users
from sara.core.utils import create_path

absolute_path = os.path.dirname(os.path.abspath(__file__))


def _save_list(path, data_list):
    """Save list to file."""
    print(f"File stored in {path}")
    with open(path, 'w') as arq:
        for data in data_list:
            arq.write(str(data['id'])+'\n')


def format_user(user):
    """Format user in np array."""
    user_stats = get_user_from_dict(user).as_dict()
    user_table = pd.DataFrame([user_stats])
    user_table = user_table.drop(columns=['id_str'])
    user = np.array(user_table)
    return user


def valid_model(model):
    """Check if the model is valid."""
    if model is None:
        raise ValueError("The SaraBotTagger model can not be None")
    path_to_model = f'{absolute_path}/bot_model/{model}'
    model = load(path_to_model)
    return True


class SaraBotTagger:
    """SaraBotTagger Class."""
    # pylint:disable=too-many-instance-attributes
    # TODO: Check the input before apply.
    def __init__(self, database, collection, limit, model):

        valid_model(model)
        # Create a path
        self.path = f'{sarabottagger_path}{collection}/'
        create_path(self.path)
        self.human_list = []
        self.bot_list = []
        self.model = load(f'{absolute_path}/bot_model/{model}')
        self.human_path = f'{self.path}human_result_{collection}.txt'
        self.bot_path = f'{self.path}bot_result_{collection}.txt'
        self.path_csv = f'{self.path}sarabottagger_result_{collection}.csv'
        self.metadata_csv = f'{self.path}sarabottagger_md_{collection}.csv'
        self.stats_path = f'{self.path}/stats_{collection}.json'
        self.database = database
        self.collection = collection
        self.limit = limit
        self.number_humans = 0
        self.number_bots = 0
        self.stats = []
        self.proba_dict = {}

    def _is_bot(self, user):
        """Check if user is a bot returning 1 or 0."""
        user = format_user(user)
        return self.model.predict(user)[0]

    def get_proba(self, user):
        """Get proba from user class."""
        user = format_user(user)
        return self.model.predict_proba(user)

    def run(self):
        """Check a number of accounts."""
        users = load_users(self.database, self.collection, self.limit)
        count = 0
        for user in users:
            print(f"checking {count}/{len(users)}")
            result = self._is_bot(user)
            class_proba = self.get_proba(user)
            human_prob = class_proba[0][0]
            bot_prob = class_proba[0][1]
            final_class = 'bot' if result == 1 else 'human'
            self.proba_dict[user['id_str']] = {'id_str': user['id_str'],
                                               'human_prob': human_prob,
                                               'bot_prob': bot_prob,
                                               'final_class': final_class}
            if result:
                user['class'] = 'bot'
                self.bot_list.append(user)
            else:
                user['class'] = 'human'
                self.human_list.append(user)
            stats = get_user_from_dict(user).as_dict()
            stats.update({"class": user['class']})
            self.stats.append(stats)
            count += 1
        _save_list(self.bot_path, self.bot_list)
        _save_list(self.human_path, self.human_list)
        self.number_humans = len(self.human_list)
        self.number_bots = len(self.bot_list)
        return self.human_list, self.bot_list, self.proba_dict

    def get_stats_dict(self):
        """Return a dict with stats."""
        sum_users = self.number_bots+self.number_humans
        percent = (self.number_bots*100)/sum_users
        return {"humans": len(self.human_list), "bots": len(self.bot_list),
                "percent_bots": percent}

    def save_csv(self):
        """Save proba dict to csv file."""
        table = pd.DataFrame(list(self.proba_dict.values()))
        table.to_csv(self.path_csv, index=False)

    def save_json(self):
        """Save json."""
        stats = self.get_stats_dict()
        stats['colecao'] = self.collection

        with open(self.stats_path, 'w', encoding="utf8") as json_file:
            json.dump(stats, json_file)


class SaraBotTaggerStandalone:
    """SaraBot Standalone Class."""

    def __init__(self, model):
        """Load bot model."""
        path_to_module = f"{absolute_path}/bot_model/{model}"
        self.model = load(path_to_module)

    def is_bot(self, user_dict):
        """Check if the user received is a bot.

        Argument: User dictionary.

        If the user is a bot return 1,
        otherwise return 0.
        """
        user = format_user(user_dict)
        return self.model.predict(user)[0]

    def is_bots(self, list_users):
        """Check a list the users.

        Argument: list[users_dict]

        Return a list if user is a bot return 1, otherwise return 0.
        """
        return [self.is_bot(user) for user in list_users]

    def is_bot_with_proba(self, user_dict):
        """Check if a account is human or bor returning proba."""
        user = format_user(user_dict)
        return self.model.predict_proba(user)
