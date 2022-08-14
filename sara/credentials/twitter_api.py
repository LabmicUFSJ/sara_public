# -*- coding: utf-8 -*-
"""
Credentials file.
Update this file with Twitter API keys
"""
import twitter
import tweepy


# auth twitter
TWITTER_KEYS = {
    'consumer_key': 'Replace with your key',
    'consumer_secret': 'Replace with your key',
    'access_token': 'Replace with your key',
    'access_token_secret': 'Replace with your key',
}

SECONDARY_TWITTER_KEYS = {
    'consumer_key': 'Replace with your key',
    'consumer_secret': 'Replace with your key',
    'access_token_key': 'Replace with your key',
    'access_token_secret': 'Replace with your key',
}


def get_twitter_api():
    """Return Twitter API connection."""
    api = twitter.Api(
        consumer_key=SECONDARY_TWITTER_KEYS['consumer_key'],
        consumer_secret=SECONDARY_TWITTER_KEYS['consumer_secret'],
        access_token_key=SECONDARY_TWITTER_KEYS['access_token_key'],
        access_token_secret=SECONDARY_TWITTER_KEYS['access_token_secret'],
        sleep_on_rate_limit=True,
        tweet_mode='extended',
    )
    return api


def get_tweepy_connector():
    """return a instance of tweepy"""
    auth = tweepy.OAuthHandler(TWITTER_KEYS['consumer_key'],
                               TWITTER_KEYS['consumer_secret'])
    auth.set_access_token(TWITTER_KEYS['access_token'],
                          TWITTER_KEYS['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True,
                     retry_count=2, retry_delay=30)
    return api
