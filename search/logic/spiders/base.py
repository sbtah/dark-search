import time
from logging import Logger
from urllib.parse import urlsplit

from httpx import Response
from logic.adapters.task import CrawlTaskAdapter
from logic.parsers.url import UrlExtractor
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from lxml.html.clean import Cleaner
from utilities.logging import logger


class BaseSpider:
    """
    Base spider containing logic for data extracting while crawling or scraping.
    """

    def __init__(self, initial_url: str, proxy: str,  user_agent: str) -> None:
        self.initial_url: str = initial_url
        self._domain: str | None = None
        self.proxy: str = proxy
        self.user_agent: str = user_agent
        self.task_adapter: CrawlTaskAdapter = CrawlTaskAdapter()
        self.url_extractor: UrlExtractor = UrlExtractor(starting_url=initial_url)
        self.logger: Logger = logger

    @staticmethod
    def now_timestamp() -> int:
        """Return integer from current timestamp."""
        return int(time.time())

    @property
    def domain(self) -> str:
        """Set domain from `initial_url`."""
        if self._domain is None:
            self._domain = urlsplit(self.initial_url).netloc
            return self._domain
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

    def page(self, response: Response) -> HtmlElement | None:
        """
        Parse response object and return HtmlElement on success.
        - :arg response: httpx Response object.
        """
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

    def extract_urls(self, html_element: HtmlElement) -> list[str] | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement.
        """
        urls = html_element.xpath('/html/body//a[@href and not(@href="")]/@href')
        if urls:
            return [url.strip() for url in urls]
        return None

    def extract_favicon_url(self, html_element: HtmlElement) -> str | None:
        """
        Search for possible favicon in head of requested page.
        - :arg html_element: Lxml HtmlElement.
        """
        # Sometimes this may be a list of urls with different icon for different resolutions.
        favicon_urls = html_element.xpath('/head/link[contains(@href, "favicon")]/@href')
        if favicon_urls:
            return favicon_urls[0].strip()
        return None

    def extract_meta_data(self, html_element: HtmlElement) -> dict:
        """
        Take HtmlElement as an input,
            return title and meta description from requested Webpage.
        - :arg html_element: Lxml HtmlElement.
        """
        title_element = html_element.xpath('/html/head/title/text()')
        description_element = html_element.xpath('/html/head/meta[@name="description"]/@content')
        meta_data = {
            'title': title_element[0].strip() if title_element else '',
            'description': description_element[0].strip() if description_element else ''
        }
        return meta_data

    def extract_page_title(self, html_element: HtmlElement) -> str | None:
        """
        Extract h1 text content from requested webpage.
        Sometimes h1 can contain other nested elements,
            because of that we want to extract entire text contained within h1 tag.
        Return parsed content.
        - :arg html_element: Lxml HtmlElement.
        """
        h1 = html_element.xpath('.//h1')
        if not h1:
            return None
        page_title = h1[0].text_content().strip()
        return page_title

    def sanitize_html_body(self, html_element: HtmlElement) -> str | None:
        """
        Extract body part from HtmlElement.
        Clean html of dangerous elements and attributes.
        """
        body = html_element.xpath('/html/body')
        cleaner = Cleaner(
                style=True,
                inline_style=True,
                scripts=True,
                javascript=True,
                embedded=True,
                frames=True,
                meta=True,
                annoying_tags=True,
                kill_tags=['img']
            )
        try:
            sanitized_content = tostring(cleaner.clean_html(body[0]))
        except Exception as e:
            self.logger.exception(f'Exception while cleaning HtmlElement: {e}')
            sanitized_content = b''
        return sanitized_content.decode('utf-8')
