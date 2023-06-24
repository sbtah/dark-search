from lxml.html import HtmlElement, HTMLParser, fromstring
from typing import List, Union
from search.utilities.logging import logger
from urllib.parse import urlsplit, urlparse, urljoin
import re


class BaseURLParser:

    def __init__(self, url, start_url=None):
        if isinstance(url, str):
            self.url = url
        else:
            raise ValueError('Please provide a string with an URL.')
        self.start_url = start_url
        self.logger = logger

    def get_domain(self, url) -> str:
        """
        Extracts domain from given URL.

        :arg url: String with URL address to parse.
        """
        try:
            domain = urlsplit(url).netloc
            return domain
        except Exception as e:
            self.logger.error(f'(get_domain) Some other exception: {e}')
            raise

    def is_onion(self, url) -> bool:
        """
        Checks if given URL is an onion URL.

        :arg url: String with URL addres to check.
        """
        try:
            domain = urlsplit(url)
            if 'onion' in domain:
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f'(is_onion) Some other Exception: {e}')
            raise

    def drop_query_params(self, url) -> str:
        """
        Cleans URL of any query params.
        Returns cleaned URL.

        :arg url: String with URL addres to check.
        """
        result = urlsplit(url)
        if result.query:
            return urljoin(url, result.path)
        return url

    def fix_paths(self, url) -> str | None:
        """
        Fixes path URL by joining it with domain.
        Returns proper URL.

        :arg url: String with URL addres to check.
        """
        if self.start_domain is not None:
            fixed_url = urljoin(self.start_domain, url)
            if self.is_valid_url(url=fixed_url):
                return fixed_url
            else:
                self.logger.info('Failed while fixing URL.')
                return None


    def is_valid_url_parse(self, url):
        """
        """
        try:
            result = urlsplit(url)
            return bool(result.scheme and result.netloc)
        except ValueError:
            return False

    def is_onion(self, url):
        """"""
        try:
            domain = urlsplit(url)
            if 'onion' in domain:
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f'(is_onion) Some other Exception: {e}')
            raise

    def is_valid_url_regex(self, url):
        """"""
        try:
            pattern = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return bool(pattern.match(url))
        except Exception as e:
            self.logger.error(f'(is_valid_url_regex) Some other Exception: {e}')
            raise


    def is_valid_url(self, url):
        """
        """
        if self.is_valid_url_parse(url) == True and self.is_valid_url_regex(url) == True:
            return True
        return False
