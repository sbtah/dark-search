import re
from typing import Iterable
from urllib.parse import SplitResult, urljoin, urlsplit


class UrlExtractor:
    """
    Url Parser is a tool designed to properly validate,
      clean and reconstruct urls found on a crawled webpage.
    Because crawler is designed to work within onion domains,
      this tool will clean url leading to clearnet.
    """

    def __init__(self, starting_url: str) -> None:
        self.starting_url: str = starting_url
        self.current_url: str | None = None
        self.current_url_split_result: SplitResult | None = None
        self.parse_results: dict[str, set] = {
            'internal': set(),
            'external': set(),
        }
        self.accepted_schemes: set[str] = {'https', 'http'}
        self._root_domain: str | None = None

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

    def is_path(self) -> bool:
        """Checks whether found url is only and path."""
        if self.current_url_split_result.path:
            return True
        return False

    def is_onion(self) -> bool:
        """Checks whether found url is leading to onion domain."""
        match = re.search(r'\S+\.onion$', self.current_url_split_result.netloc)
        if match:
            return True
        return False

    def is_accepted_scheme(self):
        """Checks whether found url contains accepted scheme."""
        if self.current_url_split_result.scheme in self.accepted_schemes:
            return True
        return False

    def clean_url(self, url: str) -> str:
        """
        Cleans current URL of all query params or fragments.
        Returns cleaned URL.
        """
        if self.current_url_split_result.query or self.current_url_split_result.fragment:
            return urljoin(self.starting_url, self.current_url_split_result.path)
        else:
            return url

    def parse(self, urls_collection: Iterable[str]):
        """
        Parse urls from provided in urls_collection.
        """
        for url in urls_collection:

            if not isinstance(url, str):
                continue

            # Set current parse result, to minimize numer of calls to urlsplit.
            self.current_url_split_result = urlsplit(url)
            # Clean url of unwanted query params and fragments.
            self.current_url = self.clean_url(url=url)

            if not self.is_valid_url() and self.is_path():
                fixed_url = urljoin(self.starting_url, self.current_url_split_result.path)
                self.current_url = fixed_url
                self.current_url_split_result = urlsplit(fixed_url)

            if not self.is_valid_url():
                continue

            if not self.is_accepted_scheme():
                continue

            if not self.is_onion():
                continue

            if self.current_url_split_result.netloc == self.root_domain:
                self.parse_results['internal'].add(self.current_url)
            else:
                self.parse_results['external'].add(self.current_url)

        return self.parse_results
