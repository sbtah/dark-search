import asyncio
import time
from typing import Iterator, List, Union

import httpx
from httpx import Response

from scout.utilities.logging import logger
from random import choice
from scout.options.settings import USER_AGENTS
from urllib.parse import urlsplit, urlparse, urljoin
from lxml.html import fromstring, HTMLParser, HtmlElement


class BaseCrawler:
    """
    Base class for all crawler logic.
    Contains basic methods for requesting URLs.
    """

    def __init__(self, page_url=None, workers=10, proxy='socks5://127.0.0.1:9050'):
        self.page_url = page_url
        self._domain = None
        self.workers = workers
        self.proxy = proxy
        self.start = int(time.time())
        self.logger = logger
        self.queue = asyncio.Queue()
        self.found_urls = set()
        self.processed_urls = set()
        self.error_urls = set()

    def page(self, response) -> Union[HtmlElement, None]:
        if response is not None:
            try:
                hp = HTMLParser(encoding='utf-8')
                self.logger.debug(
                    'Parsing text response to HtmlElement.'
                )
                element = fromstring(
                    response.text,
                    parser=hp,
                )
                return element
            except Exception as e:
                self.logger.error(f'Exception while generating HtmlElement: {e}')
                return None
        else:
            return None

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
        if self._domain is None and self.page_url is not None:
            try:
                self._domain = urlsplit(self.start_url).netloc
                return self._domain
            except Exception as e:
                raise e

    def get(self, url: str) -> Response | None:
        """
        Requests specified URL.
        Returns response object.

        :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            with httpx.Client(proxies=self.proxy) as client:
                res = client(url, headers=headers)
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
            async with httpx.AsyncClient(proxies=self.proxy) as client:
                res = await client.get(url, headers=headers)
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


    # async def search_for_urls(self, response_text):
    #     """
    #     Search for all <a> tags withing the page.
    #     Return generator of processed urls.

    #     :param response_text: Text from response object.
    #     """
    #     html_parser = self.html_parser(response_text=response_text)
    #     html_element = html_parser.generate_html_element()
    #     a_tags = html_parser.find_all_elements(
    #         html_element=html_element, xpath_to_search='.//a[@href and not(@href="")]/@href'
    #     )
    #     return a_tags
