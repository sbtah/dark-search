import re
from urllib.parse import SplitResult, urljoin, urlsplit

from logic.adapters.url import UrlAdapter
from logic.parsers.objects.url import Url


class UrlExtractor:
    """
    Url Extractor is a tool designed to properly validate,
      clean and reconstruct urls found on a crawled webpage.
    Because crawler is designed to work within onion domains,
      this tool will remove urls leading to clearnet.
    """

    def __init__(self, starting_url: Url) -> None:
        self.starting_url: Url = starting_url
        self.accepted_schemes: set[str] = {'https', 'http'}
        self._root_domain: str | None = None
        self.url_adapter: UrlAdapter = UrlAdapter()

    @property
    def root_domain(self) -> str:
        """Set root domain from 1st requested url - `starting_url`"""
        if self._root_domain is None:
            self._root_domain = urlsplit(self.starting_url.value).netloc
            return self._root_domain
        return self._root_domain

    @staticmethod
    def is_valid_url(split_result: SplitResult) -> bool:
        """
        Validates current URL by parsing it with urlsplit.
        """
        try:
            return bool(split_result.scheme and split_result.netloc)
        except ValueError:
            return False

    @staticmethod
    def is_path(path: str) -> bool:
        """Checks if the current path result is indeed valid."""
        if all([path, path != '/', path != ' ', len(path) > 1]):
            return True
        return False

    @staticmethod
    def is_onion(netloc: str) -> bool:
        """Checks whether the found url is leading to onion domain."""
        match = re.search(r'\S+\.onion$', netloc)
        if match:
            return True
        return False

    def is_accepted_scheme(self, scheme: str) -> bool:
        """Checks whether the found url contains the accepted scheme."""
        if scheme in self.accepted_schemes:
            return True
        return False

    def clean_url(self, url: str) -> str:
        """
        Cleans current URL of all query params or fragments.
        Returns cleaned URL.
        """
        split_result = urlsplit(url)
        if split_result.query or split_result.fragment:
            return urljoin(self.starting_url.value, split_result.path)
        else:
            return url

    def parse(
        self, urls_collection: list[dict[str: str, str: str]] | None
    ) -> dict[str: set[Url | None], str: set[Url | None]]:
        """
        Parse urls provided in urls_collection.
        Add internal urls to parse_results['internal'] set.
        Urls leading outside currently crawled domain (root_domain)
            are added to parse_results['external'] but only domain part.
        - :arg urls_collection: List with dictionaries representing url element from a webpage.
        """
        # Prepare parse_results dictionary.
        parse_results: dict[str: set[Url | None], str: set[Url | None]]= {
            'internal': set(),
            'external': set(),
        }
        if urls_collection is None:
            return parse_results

        for url_dict in urls_collection:

            # Extracted url after cleaning query params and fragments.
            url: str = self.clean_url(url_dict['url'])
            # # Set current parse result, to minimize numer of calls to urlsplit.
            current_url_split_result: SplitResult = urlsplit(url)
            # Extracted anchor.
            anchor: str = url_dict['anchor']

            if not self.is_valid_url(current_url_split_result) and self.is_path(current_url_split_result.path):
                fixed_url: str = urljoin(self.starting_url.value, current_url_split_result.path)
                # Set new fixed url.
                url: str = fixed_url
                # Set new split result.
                current_url_split_result: SplitResult = urlsplit(fixed_url)

            if not self.is_valid_url(current_url_split_result):
                continue

            if not self.is_accepted_scheme(current_url_split_result.scheme):
                continue

            if not self.is_onion(current_url_split_result.netloc):
                continue

            if current_url_split_result.netloc == self.root_domain:
                # Create a new url object.
                url_data: dict = {'value': url, 'anchor': anchor}
                url_obj: Url = self.url_adapter.create_url_object(**url_data)
                # Add an Url object with domain matching to starting url to the internal set.
                parse_results['internal'].add(url_obj)
            else:
                # Create a new url object.
                url_data: dict = {'value': current_url_split_result.netloc, 'anchor': anchor}
                url_obj: Url = self.url_adapter.create_url_object(**url_data)
                # Urls with domain leading outside the current domain are added to the external set.
                parse_results['external'].add(url_obj)
        return parse_results
