import asyncio
import time
from typing import Any, Dict, Iterator, List, Tuple, Union

import httpx
from httpx import Response
from logic.parsers.url import URLExtractor
from logic.spiders.base_spider import BaseSpider
from lxml.html import HtmlElement, HTMLParser, fromstring


class AsyncSpider(BaseSpider):
    """
    Asynchronous base spider.
    """

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    async def page(self, response: Response) -> Union[HtmlElement, None]:
        """
        Parses response object and returns HtmlElement on success.
        - :arg response: httpx Response object.
        """
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
            raise ValueError('Received no response')

    async def get(self, url: str) -> Response | None:
        """
        Requests specified URL. Returns Response object on success.
        - :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            async with httpx.AsyncClient(proxies=self.proxy) as client:
                res = await client.get(url, headers=headers, follow_redirects=True)
                # await asyncio.sleep(0.1)
                if res is not None:
                    return res
                else:
                    return None
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            return None

    async def get_requests(self, iterator_of_urls: Iterator) -> Tuple[Any]:
        """
        Sends requests to many urls.
        - :arg iterator_of_urls: Iterator of URLs.
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
            self.logger.error(f'(get_requests) Some other exception: {e}')
            return None

    async def request(self, url: str) -> Dict:
        """
        Requests specified url asynchronously.
        Returns dictionary with needed data.
        """
        response = await self.get(url=url)
        if response is not None:
            element = await self.page(response)
            if element is not None:
                meta_data = await self.extract_meta_data(html_element=element)
                raw_urls = await self.extract_urls(html_element=element, current_url=url)
                processed_urls = await URLExtractor(iterator_of_urls=raw_urls, current_page_url=url).process_found_urls()
                return {
                    'requested_url': str(url),
                    'responded_url': str(response.url),
                    'status': str(response.status_code),
                    'server': response.headers.get('server', None),
                    'elapsed': str(response.elapsed.total_seconds()),
                    'visited': int(time.time()) if (str(response.status_code).startswith('2') or str(response.status_code).startswith('3')) else None,
                    'meta_data': meta_data,
                    'raw_urls': raw_urls,
                    'processed_urls': list(processed_urls) if processed_urls is not None else None,
                    'content': response.content.decode('utf-8')
                }
            else:
                return {
                    'requested_url': url,
                    'status': None,
                }
        else:
            return {
                'requested_url': url,
                'status': None,
            }

    async def extract_urls(self, html_element: HtmlElement, current_url: str) -> List | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement.
        - :arg current_url: Currently requested URL, used only to generate log.
        """
        if html_element is not None:
            urls = html_element.xpath('.//body//a[@href and not(@href="") and not(starts-with(@href, "#")) and not(@href=".") and not(starts-with(@href, "mailto:")) and not(starts-with(@href , "javascript:"))]/@href')
            if urls:
                return urls
            else:
                self.logger.info(f'No urls found at: {current_url}')
                return None
        else:
            return None


    @staticmethod
    async def extract_meta_data(html_element: HtmlElement):
        """
        Takes HtmlElement as an input,
            returns title and meta description from requested Webpage.
        - :arg html_element: Lxml HtmlElement.
        """
        if html_element is not None:
            meta_data = {
                'title': html_element.xpath('/html/head/title/text()')[0].strip() if html_element.xpath('/html/head/title/text()') else '',
                'description': html_element.xpath('/html/head/meta[@name="description"]/@content')[0].strip() if html_element.xpath('./html/head/meta[@name="description"]/@content') else ''
            }
            return meta_data
