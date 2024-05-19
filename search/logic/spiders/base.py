import time
from logging import Logger

from httpx import Response
from logic.adapters.agents import UserAgentAdapter
from logic.adapters.proxy import ProxyAdapter
from logic.adapters.task import TaskAdapter
from logic.parsers.url import UrlExtractor
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from lxml.html.clean import Cleaner
from utilities.logging import logger


class BaseSpider:
    """
    Base spider containing logic for data extracting while crawling or scraping.
    """

    def __init__(self, initial_url: str) -> None:
        self.agent_adapter: UserAgentAdapter = UserAgentAdapter()
        self.proxy_adapter: ProxyAdapter = ProxyAdapter()
        self.task_adapter: TaskAdapter = TaskAdapter()
        self.url_extractor: UrlExtractor = UrlExtractor(starting_url=initial_url)
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

    @staticmethod
    def now_timestamp() -> int:
        """
        Returns integer from current timestamp.
        """
        return int(time.time())

    @property
    def user_agent(self) -> str:
        agent = self.agent_adapter.get_random_user_agent()
        return agent

    @property
    def proxy(self) -> str:
        return

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
            'User-Agent': self.user_agent,
        }

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
            return element
        except Exception as e:
            self.logger.exception(f'Exception while generating HtmlElement: {e}')
            return None

    def extract_urls(self, html_element: HtmlElement | None) -> list[str] | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement.
        """
        if html_element is None:
            return None
        urls = html_element.xpath('.//body//a[@href and not(@href="")/@href')
        if urls:
            return [url.strip() for url in urls]
        return None

    def extract_favicon_url(self, html_element: HtmlElement | None) -> str | None:
        """
        Search for possible favicon in head of requested page.
        - :arg html_element: Lxml HtmlElement.
        """
        if html_element is None:
            return None
        # Sometimes this may be a list of urls with different icon for different resolutions.
        favicon_urls = html_element.xpath('/head/link[contains(@href, "favicon")]/@href')
        if favicon_urls:
            return favicon_urls[0].strip()

    def extract_meta_data(self, html_element: HtmlElement | None) -> dict | None:
        """
        Take HtmlElement as an input,
            return title and meta description from requested Webpage.
        - :arg html_element: Lxml HtmlElement.
        """
        if html_element is not None:
            title_element = html_element.xpath('/html/head/title/text()')
            description_element = html_element.xpath('/html/head/meta[@name="description"]/@content')
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

    def sanitize_html_body(self, html_element: HtmlElement | None) -> str | None:
        """
        Extract body part from HtmlElement.
        Clean html of dangerous elements and attributes.
        """
        if html_element is None:
            return None
        body = html_element.xpath('./body')
        if body:
            cleaner = Cleaner(
                style=True,
                inline_style=True,
                scripts=True,
                javascript=True,
                embedded=True,
                frames=True,
                meta=True,
                annoying_tags=True,
            )
        try:
            sanitized_content = tostring(cleaner.clean_html(html_element))
        except Exception as e:
            self.logger.exception(f'Exception while cleaning HtmlElement: {e}')
            sanitized_content = b''
        return sanitized_content.decode('utf-8')