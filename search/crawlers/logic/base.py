import asyncio
import time
from typing import Iterator, List

import httpx
from httpx import Response

from search.utilities.logging import logger
from search.parsers.html_parser import BaseHTMLParser
from search.parsers.url_parser import BaseURLParser
from random import choice
from search.options.settings import USER_AGENTS
from urllib.parse import urlsplit, urlparse, urljoin


class BaseCrawler:
    """
    Base class for all crawler logic.
    Contains basic methods for requesting URLs.
    """

    def __init__(self, start_url, workers=10, proxy='socks5://127.0.0.1:9050'):

        self._async_client = None
        self._client = None
        self.start_url = start_url
        self._domain = None
        self.workers = workers
        self.proxy = proxy
        self.start = int(time.time())
        self.logger = logger
        self.queue = asyncio.Queue()
        self.found_urls = set()
        self.processed_urls = set()
        self.error_urls = set()

    def html_parser(self, response_text):
        return BaseHTMLParser(response_text=response_text)

    def url_parser(self, current_page_url):
        return BaseURLParser(current_page_url=current_page_url)

    async def get_proxy(self):
        pass

    @staticmethod
    def get_random_user_agent(user_agent_list: List[str]) -> str:
        """
        Returns str with random User-Agent.
        - :arg user_agent_list: List of strings with User Agents.
        """
        agent = choice(user_agent_list)
        return agent

    @property
    def user_agent(self) -> str:
        agent = self.get_random_user_agent(USER_AGENTS)
        return agent

    async def prepare_headers(self):
        pass

    @property
    def domain(self):
        if self._domain is None:
            self._domain = urlsplit(self.start_url).netloc
            return self._domain

    @property
    def async_client(self):
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(proxies=self.proxy)
            return self._async_client

    @property
    def client(self):
        if self._client is None:
            self._client = httpx.Client(proxies=self.proxy)
            return self._client

    def get(self, url: str) -> Response | None:
        """
        Requests specified URL.
        Returns response object.

        :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            res = self.client.get(url, headers=headers)
            return res
        except Exception as e:
            self.logger.error(f'(async_get) Some other exception: {e}')
            return None

    async def async_get(self, url: str) -> Response | None:
        """
        Requests specified URL.
        Returns response object.

        :param url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            res = await self.async_client.get(url, headers=headers)
            return res
        except Exception as e:
            self.logger.error(f'(async_get) Some other exception: {e}')
            return None

    async def async_get_urls(self, iterator_of_urls: Iterator):
        """
        Sends requests to iterator of urls asynchronously.

        :param iterator_of_urls: Iterator of Product URLS
            that will be used while sending requests.
        """

        tasks = []
        try:
            for url in iterator_of_urls:
                tasks.append(
                    asyncio.create_task(
                        self.async_get(
                            url,
                        )
                    )
                )
            responses = await asyncio.gather(*tasks)
            return responses
        except Exception as e:
            self.logger.error(f'(async_get_urls) Some other exception: {e}')
            raise

    async def search_for_urls(self, response_text):
        """
        Search for all <a> tags withing the page.
        Return generator of processed urls.

        :param response_text: Text from response object.
        """
        html_parser = self.html_parser(response_text=response_text)
        html_element = html_parser.generate_html_element()
        a_tags = html_parser.find_all_elements(
            html_element=html_element, xpath_to_search='.//a[@href and not(@href="")]/@href'
        )
        url_parser = self.url_parser(self.start_url)
        return url_parser.process_found_urls(a_tags)
