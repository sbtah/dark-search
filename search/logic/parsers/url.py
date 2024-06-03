import re
from urllib.parse import SplitResult, urljoin, urlsplit
from logic.objects.url import Url


class UrlExtractor:
    """
    Url Extractor is a tool designed to properly validate,
      clean and reconstruct urls found on a crawled webpage.
    Because crawler is designed to work within onion domains,
      this tool will remove urls leading to clearnet.
    """

    def __init__(self, starting_url: Url) -> None:
        self.starting_url: Url = starting_url
        self.current_url: str | None = None
        self.current_url_split_result: SplitResult | None = None
        self.accepted_schemes: set[str] = {'https', 'http'}
        self._root_domain: str | None = None

    @property
    def root_domain(self) -> str:
        """Set root domain from 1st requested url - `starting_url`"""
        if self._root_domain is None:
            self._root_domain = urlsplit(self.starting_url.value).netloc
            return self._root_domain
        return self._root_domain

    def create_url_objects(self, urls_collection: list[dict[str: str, str: str]]) -> list[Url]:
        """Convert a list of dictionaries with urls and anchors to list of Urls objects."""
        return [Url(value=data['url'], anchor=data['anchor'], number_of_requests=0) for data in urls_collection]

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
        """Checks whether the found url is leading to onion domain."""
        match = re.search(r'\S+\.onion$', self.current_url_split_result.netloc)
        if match:
            return True
        return False

    def is_accepted_scheme(self) -> bool:
        """Checks whether the found url contains the accepted scheme."""
        if self.current_url_split_result.scheme in self.accepted_schemes:
            return True
        return False

    def clean_url(self, url: Url) -> str:
        """
        Cleans current URL of all query params or fragments.
        Returns cleaned URL.
        """
        if self.current_url_split_result.query or self.current_url_split_result.fragment:
            return urljoin(self.starting_url.value, self.current_url_split_result.path)
        else:
            return url

    def parse(self, urls_collection: list[dict[str: str, str: str]] | None) -> dict:
        """
        Parse urls provided in urls_collection. Create a list of Url objects to parse.
        Add internal urls to parse_results['internal'] set.
        Urls leading outside currently crawled domain (root_domain)
            are added to parse_results['external'] but only domain part.
        """
        # Prepare parse_results dictionary.
        parse_results: dict[str: set[Url | None]] = {
            'internal': set(),
            'external': set(),
        }
        if urls_collection is None:
            return parse_results

        urls_objects_collection: list[Url] = self.create_url_objects(urls_collection=urls_collection)

        for url_obj in urls_objects_collection:

            if not isinstance(url_obj, Url):
                continue

            # Set current parse result, to minimize numer of calls to urlsplit.
            self.current_url_split_result = urlsplit(url_obj.value)
            # Clean url of unwanted query params and fragments.
            self.current_url = self.clean_url(url=url_obj.value)

            if not self.is_valid_url() and self.is_path():
                fixed_url = urljoin(self.starting_url.value, self.current_url_split_result.path)
                self.current_url = fixed_url
                self.current_url_split_result = urlsplit(fixed_url)

            if not self.is_valid_url():
                continue

            if not self.is_accepted_scheme():
                continue

            if not self.is_onion():
                continue

            if self.current_url_split_result.netloc == self.root_domain:
                # Add full internal url for possible future crawling.
                url_obj.value = self.current_url
                parse_results['internal'].add(url_obj)
            else:
                # Add domain of url leading outside the current domain.
                url_obj.value = self.current_url_split_result.netloc
                parse_results['external'].add(url_obj)
        return parse_results
