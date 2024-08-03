from collections import deque


from logic.spiders.synchronous import SyncSpider

import httpx
from httpx import Response
from logic.objects.url import Url
from logic.spiders.base import BaseSpider
from lxml.html import HtmlElement


class Probe(BaseSpider):
    """
    Probing spider used for first request.
    Saves initial data for requested domain.
    Extracts urls that will be provided to Crawler.
    """

    def __init__(self, max_retries: int = 4, *args, **kwargs) -> None:
        self.max_retries: int = max_retries
        self.queue: deque[Url] = deque()
        super().__init__(*args, **kwargs)

    def get(self, url: Url) -> tuple[Response | None, Url]:
        """
        Send request to Url.value.
        Return tuple with Response object and Url object on success.
        - :arg url: Url object.
        """
        headers: dict = self.prepare_headers()
        url.number_of_requests += 1
        try:
            with httpx.Client(
                verify=False,
                timeout=httpx.Timeout(60.0),
                follow_redirects=True,
                proxy=self.proxy,
            ) as client:
                res = client.get(url.value, headers=headers)
                return res, url
        except Exception as exc:
            self.logger.error(
                f'({SyncSpider.get.__qualname__}): Some other exception="{exc.__class__}", '
                f'message="{exc}"', exc_info=True,
            )
            return None, url

    def run_request(self, url: Url | None = None) -> tuple[Response, Url] | None:
        """
        Send get request to provided url.
        If response is not successful retry request up to max_retries.
        - :arg url: Url object.
        """
        while True:
            response: tuple[Response | None, Url] = self.get(url=url)
            if response[0] is None and url.number_of_requests < self.max_retries:
                continue
            if response[0] is not None:
                return response
        else:
            return

    def probe(self, url: Url | None = None) -> dict:
        """"""
        # Set url variable.
        url: Url = url if url is not None else self.initial_url
