import asyncio
from collections import deque
from typing import Iterable
import httpx
from httpx import Response
from logic.spiders.base import BaseSpider


class AsyncSpider(BaseSpider):
    """
    Asynchronous base spider.
    """

    def __init__(self, max_requests: int, sleep_time: float, *args, **kwargs) -> None:
        self.max_requests: int = max_requests
        self.sleep_time: float = sleep_time
        super().__init__(*args, **kwargs)

    async def get(self, url: str) -> Response:
        """
        Request specified URL.
        Return the Response object on success.
        - :arg url_dict: Dictionary with requested url.
        """
        headers = self.prepare_headers()
        try:
            async with httpx.AsyncClient(
                verify=False,
                limits=httpx.Limits(max_connections=self.max_requests),
                timeout=httpx.Timeout(60.0),
                follow_redirects=True,
                proxy=self.proxy,
            ) as client:
                res = await client.get(url, headers=headers)
                return res
        except Exception as exc:
            self.logger.error(f'(get) Some other exception: {exc}')
            return None

    async def request(self, url: str) -> dict:
        """
        Request specified url asynchronously.
        Return dictionary with needed data.
        """

        # Response from requesting a webpage. HtmlElement generated from the response text.
        response = await self.get(url)
        element = self.html_extractor.page(response) if response is not None else None

        self.logger.debug(
            f'Response: code="{response.status_code}", url="{url}", html="{True if element is not None else False}"'
        )

        if isinstance(response, Response):
            if str(response.status_code)[0] in {'2', '3'} and element is not None:
                # Parsing text prepared html element.
                parse_html_results = self.html_extractor.parse(element)
                # Parsing urls found on the webpage.
                parse_urls_results = self.url_extractor.parse(parse_html_results['on_page_urls'])
                return {
                    'requested_url': url,
                    'responded_url': str(response.url),
                    'status': str(response.status_code),
                    'server': response.headers.get('server', None),
                    'elapsed': str(response.elapsed.total_seconds()),
                    'visited': int(self.now_timestamp()),
                    'html': parse_html_results['html'],
                    'page_title': parse_html_results['page_title'],
                    'meta_title': parse_html_results['meta_title'],
                    'meta_description': parse_html_results['meta_description'],
                    'on_page_urls': parse_html_results['on_page_urls'],
                    'processed_urls': parse_urls_results,
                    'favicon_url': parse_html_results['favicon_url'],
                }
            if str(response.status_code)[0] not in {'2', '3'}:
                return {
                    'requested_url': url,
                    'responded_url': str(response.url),
                    'status': str(response.status_code),
                    'server': response.headers.get('server', None),
                    'elapsed': str(response.elapsed.total_seconds()),
                    'visited': int(self.now_timestamp()),
                    'html': f'Error: {str(response.status_code)}',
                }

        if response is None:
            return {
                'requested_url': url,
                'status': None,
            }

        if isinstance(response, httpx.HTTPError):
            return {
                'requested_url': url,
                'status': f'Exception: {response}',
            }

    async def run_requests(self, iterable_of_urls: Iterable) -> tuple[BaseException | Response] | None:
        """
        Send requests to the collection of urls.
        - :arg iterable_of_urls: Iterable of Urls that we can loop over.
        """
        # o(1) complexity
        tasks = deque()
        if iterable_of_urls is not None:
            for url in iterable_of_urls:
                # Rate limit...
                # await asyncio.sleep(self.sleep_time)
                tasks.append(
                    asyncio.create_task(self.request(url=url))
                )
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses




















