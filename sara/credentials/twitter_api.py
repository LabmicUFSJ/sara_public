# -*- coding: utf-8 -*-
"""
Credentials file.
Update this file with Twitter API keys
"""
import twitter


def get_twitter_api():
    """Return Twitter API connection."""
    api = twitter.Api(
        consumer_key='YOUR consumer_key',
        consumer_secret='YOUR consumer_secret',
        access_token_key='YOUR access_token_key',
        access_token_secret='YOUR access_token_secret',
        sleep_on_rate_limit=True,
        tweet_mode='extended',
    )
    return api
