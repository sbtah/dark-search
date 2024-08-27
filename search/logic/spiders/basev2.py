import time
from logging import Logger
from urllib.parse import urlsplit

import httpx
from httpx import Response
from logic.adapters.task import CrawlTaskAdapter
from logic.objects.url import Url
from logic.parsers.byte import Converter
from logic.parsers.html import HtmlExtractor
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
        task_id: int | str = 0,
        initial_url: Url | None = None,
        user_agent: str | None = None,
        auth_token: str | None = None,
        follow_redirects: bool = False,
        proxy: str | None = None,
        timeout_time: float | int | None = None,
        max_requests: int | None = None,
        sleep_time: float | int | None = None,
        max_retries: int | None = None,
    ) -> None:
        self.logger: Logger = logger
        self.task_id: int = task_id
        self.initial_url: Url | None = initial_url

        # Headers settings:
        self.user_agent: str | None = user_agent
        self.auth_token: str | None = auth_token

        # Client params:
        self.follow_redirects: bool = follow_redirects
        self.proxy: str | None = proxy
        # Time until timeout.
        self.timeout_time: float | int = timeout_time
        # Maximum number of clients and concurrent number of requests.
        self.max_requests: int | None = max_requests

        # Other settings:
        # Ratelimiting, sleep between requests
        self.sleep_time: float | int = sleep_time
        # Threshold for retries for Urls.
        self.max_retries: int | None = max_retries

        self._domain: str | None = None

        self.task_adapter: CrawlTaskAdapter = CrawlTaskAdapter()
        self.url_extractor: UrlExtractor = UrlExtractor(starting_url=initial_url)
        self.html_extractor: HtmlExtractor = HtmlExtractor()
        self.converter: Converter = Converter()

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

    def prepare_client_params(self) -> dict:
        """Prepare request headers for next request."""
        raise NotImplementedError

    @property
    def client(self) -> httpx.Client | httpx.AsyncClient:
        """
        Prepare instance of client for specific spider.
        """
        raise NotImplementedError

    def prepare_headers(self) -> dict:
        """
        Prepare request headers for next request.
        Reimplement on specific spider.
        """
        raise NotImplementedError

    def get(self, *, url: Url) -> tuple[Response | None, Url]:
        """
        Send request to Url.value.
        Return tuple with Response object and Url object on success.
        Reimplement on specific spider.
        - :arg url: Url object.
        """
        raise NotImplementedError
