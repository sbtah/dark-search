import asyncio
from asyncio import Future
from collections import deque
from typing import Iterable

import httpx
from httpx import Response
from logic.client.asynchronous import AsyncApiClient
from logic.parsers.objects.url import Url
from logic.spiders.base import BaseSpider
from lxml.html import HtmlElement


class AsyncSpider(BaseSpider):
    """
    Asynchronous base spider.
    """

    def __init__(self, max_requests: int, sleep_time: float | int, *args, **kwargs) -> None:
        self.max_requests: int = max_requests
        self.sleep_time: float | int = sleep_time
        self.client = AsyncApiClient()
        super().__init__(*args, **kwargs)

    async def get(self, url: Url) -> tuple[Response | None, Url]:
        """
        Send request for url value in the Url object.
        Return tuple with Response object and Url Object on success.
        - :arg url: Url object.
        """
        headers: dict = self.prepare_headers()
        url.number_of_requests += 1
        try:
            async with httpx.AsyncClient(
                verify=False,
                limits=httpx.Limits(max_connections=self.max_requests),
                timeout=httpx.Timeout(60.0),
                follow_redirects=True,
                proxy=self.proxy,
            ) as client:
                res = await client.get(url.value, headers=headers)
                # Rate limit...
                await asyncio.sleep(self.sleep_time)
                return res, url
        except Exception as exc:
            self.logger.error(
                f'({AsyncSpider.get.__qualname__}): Some other exception="{exc.__class__}", '
                f'message="{exc}"', exc_info=True
            )
            return None, url

    async def request(self, url: Url) -> dict:
        """
        Request specified url asynchronously.
        Return dictionary with needed data.
        :arg url: Url object.
        """

        # Response from requesting a webpage. HtmlElement generated from the response text.
        response: tuple[Response | None, Url] = await self.get(url)
        element: HtmlElement | None = self.html_extractor.page(response[0]) if response[0] is not None else None

        try:
            if isinstance(response[0], Response):
                self.logger.debug(
                    f'Response: status="{response[0].status_code}", url="{url}", html="{True if element is not None else False}"'
                )
                if str(response[0].status_code)[0] in {'2', '3'} and element is not None:

                    # Parsing prepared html element.
                    parse_html_results: dict = self.html_extractor.parse(element, favicon=False)
                    # Parsing urls found on the webpage.
                    parse_urls_results: dict = self.url_extractor.parse(parse_html_results['on_page_urls'])

                    return {
                        'requested_url': url,
                        'status': str(response[0].status_code),
                        'responded_url': str(response[0].url),
                        'server': response[0].headers.get('server', None),
                        'elapsed': int(response[0].elapsed.total_seconds()),
                        'visited': int(self.now_timestamp()),
                        'text': parse_html_results['text'],
                        'page_title': parse_html_results['page_title'],
                        'meta_title': parse_html_results['meta_title'],
                        'meta_description': parse_html_results['meta_description'],
                        'on_page_urls': parse_html_results['on_page_urls'],
                        'processed_urls': parse_urls_results,
                    }
                if str(response[0].status_code)[0] not in {'2', '3'} or element is None:
                    return {
                        'requested_url': url,
                        'status': str(response[0].status_code),
                        'responded_url': str(response[0].url),
                        'server': response[0].headers.get('server', None),
                        'elapsed': int(response[0].elapsed.total_seconds()),
                        'visited': int(self.now_timestamp()),
                    }

            if response[0] is None:
                self.logger.debug(
                    f'Response: status="None", url="{url}", html="{True if element is not None else False}"'
                )
                return {
                    'requested_url': url,
                    'status': None,
                }
        except Exception as e:
            self.logger.error(
                f'Response: status="Exception", class="{e.__class__}", message="{e}", '
                f'url="{url}"', exc_info=True
            )
            return {
                'requested_url': url,
                'status': None,
            }

    async def run_requests(self, iterable_of_urls: Iterable[Url]) -> list[Future]:
        """
        Send requests to the collection of urls.
        - :arg iterable_of_urls: Iterable of Urls that we can loop over.
        """
        tasks: deque = deque()
        if iterable_of_urls is not None:
            async with asyncio.TaskGroup() as tg:
                for url in iterable_of_urls:
                    tasks.append(
                        tg.create_task(self.request(url=url))
                    )
            responses = [task.result() for task in tasks]
            return responses
