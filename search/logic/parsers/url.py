import re
from re import Pattern
from urllib.parse import SplitResult, urljoin, urlsplit

from logic.adapters.url import UrlAdapter
from logic.parsers.objects.url import Url


# File pattern used in identifying urls leading to a file.
FILE_PATTERN: Pattern = re.compile(
    r"""\S+(\.zip|\.7z|\.rar|\.doc|\.docx|\.docm|\.pdf|\.ods|\.xlsx|\.xls|\.txt|\.odt|\.tgz|\.tar\.xz|
    \.tar\.Z|\.tar\.zst|\.tar\.gz|\.tar\.lz|\.tar\.bz2|\.tar|\.tlz|\.tbz2|\.txz|\.png|\.jpg|\.jpeg|
    \.csv|\.bin|\.bat|\.accdb|\.dll|\.exe|\.gif|\.mov|\.mp3|\.mp4|\.mpeg|\.mpg|\.ppt|\.pptx|\.xps|\.cbz|\.cbr)$""", re.VERBOSE
)

# Pattern for domain identification,
# for cases when href attribute will contain only a domain without a proper scheme.
DOMAIN_PATTERN: str = r'^(?=.{1,255}$)(?!-)[A-Za-z0-9\-]{1,63}(\.[A-Za-z0-9\-]{1,63})*\.?(?<!-)$'


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
        self.onion_pattern: str = r'\S+\.onion$'
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
    def split_result(url: str) -> SplitResult:
        """Split url with an urlsplit return result object."""
        return urlsplit(url)

    @staticmethod
    def join_result(url: str, path: str) -> str:
        """Return result of urljoin."""
        return urljoin(url, path)

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
        if all([len(path) > 1, path.startswith('/')]):
            return True
        if all([len(path) > 2, path.startswith('./')]):
            return True
        if all([len(path) > 3, path.startswith('../')]):
            return True
        if any([path.endswith('.html'), path.endswith('.php')]):
            return True
        return False

    @staticmethod
    def is_domain(path: str) -> bool:
        """
        Verify that scraped url is only a domain.
        Verification is happening via regex.
        :param path: Current path result of urlsplit().
        """
        domain_match = re.search(DOMAIN_PATTERN, path)
        file_match = re.search(FILE_PATTERN, path)
        if domain_match and not file_match:
            return True
        return False

    @staticmethod
    def is_file(path: str) -> bool:
        """Checks if the currently processed path is leading to a downloadable file."""
        match = re.search(FILE_PATTERN, path)
        return True if match else False

    def is_onion(self, netloc: str) -> bool:
        """Checks whether the found url is leading to onion domain."""
        match = re.search(self.onion_pattern, netloc)
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
        Cleans current URL of fragments.
        Returns cleaned URL.
        """
        split_result = self.split_result(url)
        if split_result.fragment and split_result.query:
            prepared_url = self.join_result(self.starting_url.value, split_result.path)
            return f'{prepared_url}?{split_result.query}'
        if split_result.fragment:
            prepared_url = self.join_result(self.starting_url.value, split_result.path)
            return prepared_url
        else:
            return url

    def parse_favicon_url(self, favicon_url: str | None) -> Url | None:
        """
        Parse str representing favicon url.
        Favicon urls are usually a path urls,
        this method is building a full url and converting it to the Url object.
        - :arg favicon_url: String if favicon url was successfully extracted.
        """
        if favicon_url is None:
            return None

        split_result: SplitResult = self.split_result(favicon_url)

        if not self.is_valid_url(split_result) and self.is_path(split_result.path):
            favicon_url_str: str = self.join_result(self.starting_url.value, favicon_url)
            favicon_url_obj: Url = self.url_adapter.create_url_object(value=favicon_url_str)
            return favicon_url_obj
        return self.url_adapter.create_url_object(value=favicon_url)

    def parse(
        self, urls_collection: list[dict[str, str], ...] | None
    ) -> dict[str, set[Url]]:
        """
        Parse urls provided in urls_collection.
        Add internal urls to parse_results['internal_urls'] set.
        Urls leading outside currently crawled domain (root_domain)
            are added to parse_results['external_urls']
        - :arg urls_collection: List with dictionaries representing url elements from a webpage.
        """
        # Prepare parse_results dictionary.
        parse_results: dict[str, set[Url]] = dict(internal_urls=set(), external_urls=set())
        if urls_collection is None:
            return parse_results

        for url_dict in urls_collection:

            # Extracted url after cleaning query params and fragments.
            url: str = self.clean_url(url_dict['url'])
            # # Set current parse result, to minimize numer of calls to urlsplit.
            current_url_split_result: SplitResult = self.split_result(url)
            # Extracted anchor.
            anchor: str = url_dict['anchor']

            # Repairing paths and query urls, by joining them with starting_url.
            if not self.is_valid_url(current_url_split_result) and self.is_path(current_url_split_result.path) and current_url_split_result.query:
                fixed_url: str = self.join_result(self.starting_url.value, f'{current_url_split_result.path}?{current_url_split_result.query}')
                # Set new fixed url.
                url = fixed_url
                # Set new split result.
                current_url_split_result = self.split_result(fixed_url)

            # Repairing paths only urls, by joining them with starting_url.
            if not self.is_valid_url(current_url_split_result) and self.is_path(current_url_split_result.path):
                fixed_url = self.join_result(self.starting_url.value, current_url_split_result.path)
                # Set new fixed url.
                url = fixed_url
                # Set new split result.
                current_url_split_result = self.split_result(fixed_url)

            # Repairing urls without a scheme. Urlsplit will categorize these as paths.
            if not self.is_valid_url(current_url_split_result) and self.is_domain(current_url_split_result.path):
                fixed_url = f'http://{current_url_split_result.path}'
                url = fixed_url
                current_url_split_result = self.split_result(fixed_url)

            if not self.is_valid_url(current_url_split_result):
                continue

            if not self.is_accepted_scheme(current_url_split_result.scheme):
                continue

            if self.is_file(current_url_split_result.path):
                continue

            if not self.is_onion(current_url_split_result.netloc):
                continue

            url_data: dict = {'value': url, 'anchor': anchor}
            if current_url_split_result.netloc == self.root_domain:
                # Create a new url object.
                url_obj: Url = self.url_adapter.create_url_object(**url_data)
                # Add an Url object with domain matching to starting url to the internal set.
                parse_results['internal_urls'].add(url_obj)
            else:
                # Create a new url object.
                url_obj = self.url_adapter.create_url_object(**url_data)
                # Urls with domain leading outside the current domain are added to the external set.
                parse_results['external_urls'].add(url_obj)

        return parse_results
