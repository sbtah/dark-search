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

    async def get(self, url: str) -> Response | None:
        """
        Request specified URL. Return Response object on success.
        - :arg url: Requested URL.
        """
        headers = self.prepare_headers()
        try:
            async with httpx.AsyncClient(verify=False, timeout=30, max_redirects=1, proxy=self.proxy) as client:
                res = await client.get(url, headers=headers, follow_redirects=True)
                await asyncio.sleep(self.sleep_time)
                if not res:
                    return None
                return res
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            return None

    async def run_requests(self, iterable_of_urls: Iterable) -> deque[dict]:
        """
        Send requests to collection of urls.
        - :arg iterable_of_urls: Iterable of Urls that we can loop over.
        """
        # o(1) complexity
        tasks = deque()
        try:
            for url in iterable_of_urls:
                tasks.append(
                    asyncio.create_task(
                        self.request(
                            url,
                        )
                    )
                )
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses
        except Exception as e:
            self.logger.error(f'(run_requests) Some other exception: {e}')
            return None

    async def request(self, url: str) -> dict:
        """
        Request specified url asynchronously.
        Returns dictionary with needed data.
        """
        # Response from requesting a webpage.
        response = await self.get(url=url)

        # Parsed response
        parsed_response = {
            'requested_url': url,
            'status': None,
        }

        if not response:
            return parsed_response

        # Generate HtmlElement.
        element = self.page(response)
        extra_parsed_response = {
            'responded_url': str(response.url),
            'status': str(response.status_code),
            'server': response.headers.get('server', None),
            'elapsed': str(response.elapsed.total_seconds()),
            'visited': int(self.now_timestamp()),
            'html': 'NO HTML',
        }
        if element is None or str(response.status_code)[0] not in {'2', '3'}:
            return {**parsed_response, **extra_parsed_response}

        # Extract data from requested page.
        page_title: str | None = self.extract_page_title(html_element=element)
        # print(f'DEBUG TITLE : {page_title}')
        meta_data: dict | None = self.extract_meta_data(html_element=element)
        # print(f'DEBUG META : {meta_data}')
        raw_urls: list = self.extract_urls(html_element=element)
        # print(f'DEBUG RAW URLS : {raw_urls}')
        cleaned_html_body: str = self.sanitize_html_body(html_element=element)
        # print(f'DEBUG HTML: {cleaned_html_body}')
        processed_urls: dict = self.url_extractor.parse(urls_collection=raw_urls)
        # print(f'DEBUG processed URLS: {processed_urls}')
        html_parsed_response = {
            'html': cleaned_html_body,
            'page_title': page_title,
            'meta_data': meta_data,
            'raw_urls': raw_urls,
            'processed_urls': processed_urls,
        }

        return {**parsed_response, **extra_parsed_response, **html_parsed_response}