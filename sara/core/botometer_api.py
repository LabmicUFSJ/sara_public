# -*- coding: utf-8 -*-
"""Methods related to botometer"""

import botometer

from sara.credentials.botometer_credentials import rapidapi_key
from sara.credentials.twitter_api import TWITTER_KEYS

BOM = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **TWITTER_KEYS)


def check_users_botometer(list_users):
    """Check users in botometer API.
    Return a dictionary with recovered data from botometer.
    """
    return dict(BOM.check_accounts_in(list_users))


def check_user_botometer(user_id):
    """Check user in botometer API."""
    return BOM.check_account(user_id)
