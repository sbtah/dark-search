from typing import Iterator
from urllib.parse import urlsplit, urljoin, SplitResult
import re
from utilities.logging import logger


class UrlExtractor:
    """
    Url Parser is a tool designed to properly validate,
      clean and reconstruct urls found on a crawled webpage.
    Because crawler is designed to work within onion domains,
      this tool will clean url leading to clearnet.
    """

    def __init__(self, starting_url: str, urls_collection: Iterator[str] = None) -> None:
        self.urls_collection: Iterator[str] | None = urls_collection
        self.starting_url: str = starting_url
        self.current_url: str | None = None
        self.current_url_split_result: SplitResult | None = None
        self.parse_results: dict[str, set] = {
            'internal': set(),
            'external': set(),
        }
        self.accepted_schemes: set[str] = {'https', 'http'}
        self.accepted_domain_extensions: set[str] = {'.onion'}
        self._root_domain: str | None = None
        self.logger = logger

    @property
    def root_domain(self) -> str:
        """
        Set root domain from 1st requested url - `starting_url`
        """
        if self._root_domain is None:
            self._root_domain = urlsplit(self.starting_url).netloc
            return self._root_domain
        return self._root_domain

    def is_valid_url(self) -> bool:
        """
        Validates current URL by parsing it with urlsplit.
        """
        try:
            return bool(self.current_url_split_result.scheme and self.current_url_split_result.netloc)
        except ValueError:
            return False

    def clean_url(self) -> str:
        """
        Cleans current URL of all query params or fragments.
        Returns cleaned URL.
        """
        try:
            if self.current_url_split_result.query or self.current_url_split_result.fragment:
                return urljoin(self.root_domain, self.current_url_split_result.path)
            else:
                return self.current_url
        except Exception as e:
            self.logger.error(f'(clean_url) Some other Exception: {e}')
            raise

    def parse(self):
        """
        Parse urls from self.urls_collection.
        """
        for url in self.urls_collection:

            self.current_url = url
            # Set current parse result, to minimize numer of calls to urlsplit.
            self.current_url_split_result = urlsplit(url)

            if not self.is_valid_url():
                ...

    def is_valid_url(self) -> bool:
        """
        Validates current URL by parsing it with urlsplit.
        """
        try:
            return bool(self.current_url_split_result.scheme and self.current_url_split_result.netloc)
        except ValueError:
            return False

    # def is_valid_url_regex(self, url: str) -> bool:
    #     """
    #     Validates URL by Regex.

    #     :arg url: String with URL address to check.
    #     """
    #     try:
    #         pattern = re.compile(
    #             r'^(?:http|ftp)s?://'
    #             r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    #             r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    #             r'(?::\d+)?'
    #             r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    #         return bool(pattern.match(url))
    #     except Exception as e:
    #         self.logger.error(f'(is_valid_url_regex) Some other Exception: {e}')
    #         raise

    def is_valid_url(self, url: str) -> bool:
        """
        Validates URL by parsing and Regex.
        Returns bool.

        :arg url: String with URL address to check.
        """
        if self.is_valid_url_parse(url) is True and self.is_valid_url_regex(url) is True:
            return True
        return False

    def is_path(self, url):
        ...
