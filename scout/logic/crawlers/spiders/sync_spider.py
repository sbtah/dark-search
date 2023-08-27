from typing import Iterator, Union, Dict

import httpx
from lxml.html import HtmlElement, HTMLParser, fromstring

from logic.crawlers.spiders.base_spider import BaseSpider
from logic.parsers.url import URLExtractor


class SyncSpider(BaseSpider):
    """
    Synchronous base spider.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_response = None

    def page(self, response) -> Union[HtmlElement, None]:
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

    def get(self, url: str) -> Dict | None:
        """
        Requests specified URL. Returns HtmlElement on successful response.
        :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            with httpx.Client(proxies=self.proxy) as client:
                res = client.get(url, headers=headers, follow_redirects=True)
                self._last_response = res
                element = self.page(res)
                return {
                    'status': res.status_code,
                    'server': res.headers['server'],
                    'elapsed': res.elapsed.total_seconds(),
                    'page': element,
                }
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            return None

    def get_urls(self, iterator_of_urls: Iterator):
        """
        Sends requests to iterator of urls synchronously.
        :param iterator_of_urls: Iterator of Product URLS
            that will be used while sending requests.
        """
        try:
            for url in iterator_of_urls:
                response = self.get(url=url)
                yield response
        except Exception as e:
            self.logger.error(f'(get_urls) Some other exception: {e}')
            raise

    def search_for_urls(self, response):
        """"""
        if response is not None:
            urls = response['page'].xpath('.//body//a[@href and not(@href="")]/@href')
            if urls:
                extractor = URLExtractor(iterator_of_urls=urls, current_page_url=self._initial_url)
                print(extractor.process_found_urls())