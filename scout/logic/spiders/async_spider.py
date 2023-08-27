import asyncio
from typing import Iterator, Union, Dict, List

import httpx
from lxml.html import HtmlElement, HTMLParser, fromstring

from logic.spiders.base_spider import BaseSpider
from logic.parsers.url import URLExtractor


class AsyncSpider(BaseSpider):
    """
    Asynchronous base spider.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_response = None
        self._last_requested_url = None

    async def page(self, response) -> Union[HtmlElement, None]:
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
                raise e
        else:
            raise ValueError(f'Received bad response of type: {type(response)}')

    async def get(self, url: str) -> Dict | None:
        """
        Requests specified URL. Returns HtmlElement on successful response.
        :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            async with httpx.AsyncClient(proxies=self.proxy) as client:
                res = await client.get(url, headers=headers, follow_redirects=True)
                if res is not None:
                    return res
                else:
                    return None
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            return None

    async def request(self, url):
        response = await self.get(url=url)
        if response is not None:
            self._last_response = response
            self._last_requested_url = url
            element = await self.page(response)
            return {
                'status': response.status_code,
                'server': response.headers['server'],
                'elapsed': response.elapsed.total_seconds(),
                'file': True if response.headers.get('content-length') else False,
                'raw_urls': await self.search_for_urls(html_element=element, current_url=url),
            }
        else:
            self.logger.error(f'No response received from: {url}')
            return {'status': None}

    async def get_urls(self, iterator_of_urls: Iterator) -> Dict:
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
                        self.request(
                            url,
                        )
                    )
                )
            responses = await asyncio.gather(*tasks)
            return responses
        except Exception as e:
            self.logger.error(f'(get_urls) Some other exception: {e}')
            raise

    async def search_for_urls(self, html_element: HtmlElement, current_url: str) -> List[str|None]:
        """
        Search for urls in body of provided HtmlElement.
        :param html_element: Lxml HtmlElement.
        :param current_url: Currently requested URL.
        """
        if html_element is not None:
            urls = html_element.xpath('.//body//a[@href and not(@href="") and not(@href="#") and not(@href=".")]/@href')
            if urls:
                return urls
            else:
                self.logger.info(f'No urls found at: {current_url}')
                return None