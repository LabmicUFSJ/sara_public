""" Exceptions file"""
from requests.exceptions import RequestException


class SaraRequestException(RequestException, Exception):
    """Fail to make a web request."""
