import copy
import time
from logging import Logger
from urllib.parse import urlsplit

from logic.adapters.task import CrawlTaskAdapter
from logic.parsers.byte import Converter
from logic.parsers.html import HtmlExtractor
from logic.objects.url import Url
from logic.parsers.url import UrlExtractor
from utilities.log import logger


class BaseSpider:
    """
    Base spider containing logic for data extracting while crawling or scraping.
    Each spider inheriting from this class expects to receive UserAgent and Proxy,
    as well as initial url object.
    """

    def __init__(
        self,
        *,
        initial_url: Url,
        proxy: str,
        user_agent: str,
        sleep_time: float | int,
        max_retries: int,
        timeout_time: float | int,
    ) -> None:
        self.initial_url: Url = initial_url
        self._domain: str | None = None
        self.proxy: str = proxy
        self.user_agent: str = user_agent
        self.task_adapter: CrawlTaskAdapter = CrawlTaskAdapter()
        self.url_extractor: UrlExtractor = UrlExtractor(starting_url=initial_url)
        self.html_extractor: HtmlExtractor = HtmlExtractor()
        self.converter: Converter = Converter()
        self.logger: Logger = logger
        # Ratelimiting sleep between requests
        self.sleep_time: float | int = sleep_time
        # Threshold for retries for Urls.
        self.max_retries: int = max_retries
        # Timeout for get request.
        self.timeout_time: float | int = timeout_time

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
