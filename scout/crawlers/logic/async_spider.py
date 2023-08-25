import asyncio
from typing import Iterator, Union, Dict

import httpx
from lxml.html import HtmlElement, HTMLParser, fromstring

from crawlers.logic.base_spider import BaseSpider


class AsyncSpider(BaseSpider):
    """
    Asynchronous base spider.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_response = None

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
                self._last_response = res
                element = await self.page(res)
                return {
                    'status': res.status_code,
                    'server': res.headers['server'],
                    'elapsed': res.elapsed.total_seconds(),
                    'page': element,
                }
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            return None

    async def get_urls(self, iterator_of_urls: Iterator):
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
                        self.get(
                            url,
                        )
                    )
                )
            elements = await asyncio.gather(*tasks)
            return elements
        except Exception as e:
            self.logger.error(f'(get_urls) Some other exception: {e}')
            raise
