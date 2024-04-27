import time
from random import choice

from typing import Any, Dict, Iterator, List, Tuple, Union
from httpx import Response
from dotenv import load_dotenv

from logic.adapters.task import TaskAdapter
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from logic.parsers.url import UrlExtractor
from utilities.logging import logger
from logging import Logger


class BaseSpider:
    """
    Base class for all spiders.
    """

    def __init__(self) -> None:

        self.user_agent_adapter = ...
        self.proxy_adapter = ...
        self.task_adapter: TaskAdapter = TaskAdapter()
        self.logger: Logger = logger

        # TODO :
        # Move do dedicated spider.

        # self.initial_url = initial_url
        # self.url_extractor = UrlExtractor(starting_url=initial_url)
        # self.found_internal_urls = set()
        # self.external_domains = set()
        # self.requested_urls = set()
        # self.max_requests = 10
        # self.sleep_time = 5
        # self.site_structure = {}

        # TODO:
        # Move to launcher:
        # self.crawl_start: int = int(time.time())
        # self.crawl_end: int | None = None

    # @property
    # def user_agent(self) -> str:
    #     agent = self.get_random_user_agent(USER_AGENTS)
    #     return agent

    # @staticmethod
    # def get_random_user_agent(user_agent_list: List[str]) -> str:
    #     """
    #     Returns str with random User-Agent.
    #     - :arg user_agent_list: List of strings with User Agents.
    #     """
    #     agent = choice(user_agent_list)
    #     return agent

    def page(self, response: Response) -> HtmlElement | None:
        """
        Parses response object and returns HtmlElement on success.
        - :arg response: httpx Response object.
        """
        if response is None:
            raise ValueError('Received no response')
        try:
            hp = HTMLParser(encoding='utf-8')
            element = fromstring(
                response.text,
                parser=hp,
            )
            self.logger.debug(f'')
            return element

        
        except Exception as e:
            self.logger.exception(f'Exception while generating HtmlElement: {e}')
            return None

    def extract_urls(self, html_element: HtmlElement | None) -> List | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement.
        - :arg current_url: Currently requested URL, used only to generate log.
        """
        if html_element is None:
            return None
        urls = html_element.xpath('.//body//a[@href and not(@href="")/@href')
        if urls:
            return [url.strip() for url in urls]
        return None

    def extract_meta_data(self, html_element: HtmlElement | None) -> Dict | None:
        """
        Take HtmlElement as an input,
            return title and meta description from requested Webpage.
        - :arg html_element: Lxml HtmlElement.
        """
        if html_element is not None:
            title_element = html_element.xpath('/html/head/title/text()')
            description_element = html_element.xpath('./html/head/meta[@name="description"]/@content')
            meta_data = {
                'title': title_element[0].strip() if title_element else '',
                'description': description_element[0].strip() if description_element else ''
            }
            return meta_data
        return None

    def extract_page_title(self, html_element: HtmlElement | None) -> str | None:
        """
        Extract h1 text content from requested webpage.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        if html_element is None:
            return None
        h1 = html_element.xpath('.//h1')
        if h1:
            page_title = html_element.xpath('.//h1')[0].text_content().strip()
            return page_title
        return None


    @staticmethod
    def now_timestamp():
        """
        Returns integer from current timestamp.
        """
        return int(time.time())

    # TODO:
    # Prepare proper header to mimic browser.
    def prepare_headers(self):
        pass
