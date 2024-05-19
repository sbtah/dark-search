import asyncio
from typing import Any, Dict, Iterable, List, Tuple, Union
from logic.parsers.html import sanitize_html
import httpx
from httpx import Response
from logic.spiders.base import BaseSpider
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from logic.parsers.url import UrlExtractor


class AsyncSpider(BaseSpider):
    """
    Asynchronous base spider.
    """

    def __init__(self, initial_url: str, max_requests: int, sleep_time: float, *args, **kwargs) -> None:
        self.initial_url = initial_url
        self.url_extractor = UrlExtractor(starting_url=initial_url)
        self.found_internal_urls = set()
        self.external_domains = set()
        self.requested_urls = set()
        self.max_requests = max_requests
        self.sleep_time = sleep_time
        self.site_structure = {}
        super().__init__(*args, **kwargs)


    async def ratelimit_urls(self, urls: List):
        """
        My implementation of limiting number of requests send.
        I'm simply splitting received iterator of urls,
            to list of list with length of self.max_requests.
        Generate list of urls lists.
        """
        if len(urls) > self.max_requests:
            return [
                urls[x: x + self.max_requests] for x in range(0, len(urls), self.max_requests)
            ]
        else:
            return [urls, ]


    async def get(self, url: str) -> Response | None:
        """
        Requests specified URL. Returns Response object on success.
        - :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            async with httpx.AsyncClient(proxies=self.proxy) as client:
                res = await client.get(url, headers=headers, follow_redirects=True)
                await asyncio.sleep(self.sleep_time)
                if not res:
                    return None
                return res
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            return None

    async def run_requests(self, iterable_of_urls: Iterable):
        """
        Sends requests to collection of urls.
        - :arg iterator_of_urls: Iterator of URLs.
        """
        tasks = []
        try:
            for url in iterable_of_urls:
                tasks.append(
                    asyncio.create_task(
                        self.request(
                            url,
                        )
                    )
                )
            responses = await asyncio.gather(*tasks)
            return responses
        except Exception as e:
            self.logger.error(f'(run_requests) Some other exception: {e}')
            return None

    async def request(self, url: str) -> Dict:
        """
        Requests specified url asynchronously.
        Returns dictionary with needed data.
        """
        response = await self.get(url=url)
        if not response:
            return {
                'requested_url': url,
                'status': None,
            }

        element = self.page(response)
        if not element:
            return {
                'requested_url': url,
                'status': None,
            }

        page_title = self.extract_page_title(html_element=element)
        meta_data = self.extract_meta_data(html_element=element)
        raw_urls = self.extract_urls(html_element=element)
        cleaned_html_body = self.sanitize_html_body(html_element=element)
        processed_urls = self.url_extractor.parse(urls_collection=raw_urls)
        return {
            'requested_url': str(url),
            'responded_url': str(response.url),
            'status': str(response.status_code),
            'server': response.headers.get('server', None),
            'elapsed': str(response.elapsed.total_seconds()),
            'visited': int(self.now_timestamp()) if (str(response.status_code).startswith('2') or str(response.status_code).startswith('3')) else None,
            'html': cleaned_html_body,
            'page_title': page_title,
            'meta_data': meta_data,
            'raw_urls': raw_urls if raw_urls else None,
            'processed_urls': list(processed_urls) if processed_urls is not None else None,
        }
