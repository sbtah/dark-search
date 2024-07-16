import copy
import time
from logging import Logger
from urllib.parse import urlsplit

from logic.adapters.task import CrawlTaskAdapter
from logic.parsers.byte import Converter
from logic.parsers.html import HtmlExtractor
from logic.parsers.objects.url import Url
from logic.parsers.url import UrlExtractor
from utilities.log import logger


class BaseSpider:
    """
    Base spider containing logic for data extracting while crawling or scraping.
    Each spider inheriting from this class expects to receive UserAgent and Proxy,
    as well as initial url object.
    """

    def __init__(self, initial_url: Url, proxy: str, user_agent: str) -> None:
        self.initial_url: Url = initial_url
        self._domain: str | None = None
        self.proxy: str = proxy
        self.user_agent: str = user_agent
        self.task_adapter: CrawlTaskAdapter = CrawlTaskAdapter()
        self.url_extractor: UrlExtractor = UrlExtractor(starting_url=initial_url)
        self.html_extractor: HtmlExtractor = HtmlExtractor()
        self.converter: Converter = Converter()
        self.logger: Logger = logger

    @staticmethod
    def now_timestamp() -> int:
        """Return integer from current timestamp."""
        return int(time.time())

    @property
    def domain(self) -> str:
        """Set domain from `initial_url`."""
        if self._domain is None:
            self._domain = urlsplit(self.initial_url.value).netloc
        return self._domain

    def prepare_headers(self) -> dict:
        """Prepare request headers for next request."""
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'close',
            'User-Agent': self.user_agent,
        }

    @staticmethod
    def serialized_response(response_dict: dict) -> dict:
        """
        Make a copy of response and change Url objects in response to dictionary.
        Used while sending data to the API.
        """

        copied_response: dict = copy.deepcopy(response_dict)
        url: Url = copied_response.pop('requested_url')
        url = url.serialize()
        serialized_response: dict = {'requested_url': url, **copied_response}

        if copied_response.get('processed_urls') is None:
            return serialized_response

        processed_urls: dict[str, set[Url]] = copied_response.pop('processed_urls')
        processed_urls_new: dict = dict()

        if len(processed_urls['internal_urls']) > 0:
            internal_set: set[Url] = processed_urls.pop('internal_urls')
            new_internal: list[dict] = [url_obj.serialize() for url_obj in internal_set]
            processed_urls_new['internal'] = new_internal

        if len(processed_urls['external_urls']) > 0:
            external_set: set[Url] = processed_urls.pop('external_urls')
            new_external: list[dict] = [url_ob.serialize() for url_ob in external_set]
            processed_urls_new['external'] = new_external

        serialized_response = {'requested_url': url, **copied_response, 'processed_urls': processed_urls_new}
        return serialized_response
