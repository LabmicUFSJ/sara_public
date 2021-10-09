# -*- coding: utf-8 -*-
"""
Log
"""
import logging
import time
from datetime import datetime


def get_log():
    """Set configurations related to LOG."""
    # create logger
    logging.basicConfig(filename='sara.log', level=logging.WARNING)
    logger = logging.getLogger('sara_log')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter
    pattern_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(pattern_formatter)
    logging.Formatter.converter = time.gmtime
    # add formatter to console_handler
    console_handler.setFormatter(formatter)

    # add console_handler to logger
    logger.addHandler(console_handler)
    return logger


def keyword_log(keywords, file="log_keywords.txt"):
    """Save keywords used to retrieve tweets from Twitter API."""
    print("Log init ok")
    now = datetime.utcnow()
    current_time = now.strftime("%H:%M:%S - %d/%m/%Y")
    msg = ": " + str(keywords) + "- Begin: " + current_time + " - UTC "+"\n"
    with (open(file, "a+")) as archive:
        archive.write(msg)
