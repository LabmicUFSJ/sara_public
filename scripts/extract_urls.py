# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
URL analysis.

Extract URLS from Tweets hosted on MongoDB.

- USE MONGODB

Save the result as a CSV file.
"""
# System import
import re
import sys
from collections import Counter
from pathlib import Path

# library import
import pandas as pd

# Local import
from sara.core.config import DEFAULT
from sara.core.sara_data import SaraData
from sara.core.utils import create_path, get_web_url, load_txt


def get_match_obj(url_pattern, patterns_list):
    """Return re.match object."""
    pattern = r'(http[s]*://)(' + url_pattern + r')[\D\d]+'
    patterns_list.append(re.compile(pattern))
    return patterns_list


def generate_patterns():
    """Generate list with regex match objs to match with website urls."""
    patterns = []
    # bit.ly
    patterns = get_match_obj('bit.ly', patterns)
    # http://zpr.io/
    patterns = get_match_obj('zpr.io', patterns)
    # http://chng.it/
    patterns = get_match_obj('chng.it', patterns)
    # dlvr.it
    patterns = get_match_obj('dlvr.it', patterns)
    # buff
    patterns = get_match_obj('buff.ly', patterns)
    # glob
    patterns = get_match_obj('glo.bo', patterns)
    # ow.ly
    patterns = get_match_obj('ow.ly', patterns)
    # mlab.bs
    patterns = get_match_obj('mla.bs', patterns)
    # cnn
    patterns = get_match_obj('cnn.it', patterns)
    # is.gd
    patterns = get_match_obj('is.gd', patterns)
    # disq
    patterns = get_match_obj('disq.us', patterns)
    # wpp
    patterns = get_match_obj('wp.me', patterns)
    # tinyurl
    patterns = get_match_obj('tinyurl.com', patterns)
    # go.shr
    patterns = get_match_obj('go.shr.lc', patterns)
    # goo.gl
    patterns = get_match_obj('goo.gl', patterns)
    # migre.me
    patterns = get_match_obj('migre.me', patterns)
    return patterns


PATTERNS = generate_patterns()


def _get_url(expanded_url):
    """Format bit.ly link to be translated into a 'real' web link

    Translate from bit.ly to 'real' web link.
    """
    for pattern in PATTERNS:

        if pattern.match(expanded_url):
            return get_web_url(expanded_url)

    return expanded_url


def extract_urls(tweets, exclude_pattern):
    """Extract urls from twitter data."""
    extracted_urls = []
    twitter_pattern = r'(http[s]*://)(twitter.com)[\D\d]+'

    for tweet in tweets:
        temp = set()
        if tweet.get("retweeted_status"):
            for url in tweet["retweeted_status"]['entities']['urls']:
                expanded_url = url['expanded_url']
                if re.match(twitter_pattern, url['expanded_url']):
                    continue
                if re.match(exclude_pattern, expanded_url):
                    continue
                temp.add(expanded_url)
        if tweet.get('entities'):
            for url in tweet['entities']['urls']:
                expanded_url = url['expanded_url']
                if re.match(twitter_pattern, url['expanded_url']):
                    continue
                if re.match(exclude_pattern, expanded_url):
                    continue
                temp.add(expanded_url)
        for temp_url in temp:
            extracted_urls.append(temp_url)
    return extracted_urls


def get_inputed_data():
    """Check inputed data."""
    path_to_ids = None
    try:
        collection_name = sys.argv[1]
        if len(sys.argv) == 3:
            path_to_ids = sys.argv[2]
    except (IndexError, TypeError) as error:
        print(f'Error {error}')
        print(f"Please, input python {sys.argv[0]} <collection_name> "
              "<path_to_ids>")
        print("If path to ids is not defined run without filter by ids.")
        sys.exit(-1)
    return collection_name, path_to_ids


def _counter_links(urls):
    """Count the number of times the a URL is present."""
    # Generate a dict used to make translate the bit.ly links to real link
    dict_urls = {i: '' for i in urls}

    # Remove shortener from link.
    # Translate bit.ly links to 'real' link.
    uncut_urls_dict = {key: _get_url(key) for key, _ in dict_urls.items()}

    urls_list = [uncut_urls_dict[i] for i in urls]

    # Count the number of the repeated links
    counter = Counter(urls_list)
    urls = [[key, value] for key, value in counter.items()]
    urls = sorted(urls, key=lambda item: item[1], reverse=True)
    return urls


def get_urls_by_ids(collection_name, ids, exclude_pattern=r'[\D0-9]+(go.jp)'):
    """Get urls from ids."""
    data = SaraData(collection_name)
    project = {"retweeted_status.entities.urls": 1,
               "entities.urls": 1, "user.id_str": 1}

    urls = []

    for usr_id in ids:
        # Filter to recovery links
        filter_user = {"user.id_str": usr_id, 'lang': 'pt'}
        tweets = data.get_filtered_tweet(filter_user, project, 0)
        recovered = data.count_recovered_documments(filter_user, 1)
        if recovered:
            rec_url = extract_urls(tweets, exclude_pattern)
            urls = urls + rec_url
        else:
            filter_user = {"retweeted_status.user.id_str": usr_id,
                           'lang': 'pt'}
            project = {"retweeted_status.entities.urls": 1,
                       "entities.urls": 1, "retweeted_status.user.id_str": 1}
            tweets = data.get_filtered_tweet(filter_user, project, 0)
            recovered = data.count_recovered_documments(filter_user, 1)
            if recovered:
                rec_url = extract_urls(tweets, exclude_pattern)
                urls = urls + rec_url
    print(f'Extracted links {urls}')
    return _counter_links(urls)


def main(collection_name, exclude_pattern=r'[\D0-9]+(go.jp)'):
    """URL analysis."""
    data = SaraData(collection_name)

    project = {"retweeted_status.entities.urls": 1, "entities.urls": 1}

    tweet_filter = {"lang": 'pt'}
    tweets = data.get_filtered_tweet(tweet_filter, project, 0)

    urls = extract_urls(tweets, exclude_pattern)
    return _counter_links(urls)


if __name__ == "__main__":

    PATH_TO_SAVE = DEFAULT + "url_analysis/"
    create_path(PATH_TO_SAVE)
    collections, path_to_users = get_inputed_data()
    COUNTER_URLS = None
    if not path_to_users:
        COUNTER_URLS = main(collections)
    else:
        users_ids = load_txt(path_to_users)
        COUNTER_URLS = get_urls_by_ids(collections, users_ids)
    table = []
    for url_shared in COUNTER_URLS:
        if re.match(r'(http[s]*://)(twitter.com)[\D\d]+', url_shared[0]):
            continue
        table.append({"url": url_shared[0], "shared_count": url_shared[1],
                     "subject": collections})
    pandas_table = pd.DataFrame(table)
    if path_to_users:
        users_path = Path(path_to_users)
        files_name = users_path.name.replace('.txt', '')
        collections = collections + f"_{files_name}"
    PATH_TO_SAVE = f"{PATH_TO_SAVE}{collections}.csv"
    pandas_table.to_csv(PATH_TO_SAVE, index=False)
    print(f"Saved file: {PATH_TO_SAVE}")
    print(len(table))
