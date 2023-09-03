from logic.spiders.async_spider import AsyncSpider
from logic.parsers.url import URLExtractor
from typing import Iterator
import asyncio


class BaseCrawler:

    def __init__(self, found_urls=None):
        self.spider = AsyncSpider()
        self.url_extractor = URLExtractor
        self.client = None
        self.found_urls = found_urls if found_urls is not None else set()
        self.requested_urls = set()
        self.max_requests = 5
        self.sleep_time = 2

    async def crawl(self):

        # My manual implementation of limiting requests.
        lists_of_urls_list = self.limited_urls_iterators(list(self.found_urls))

        for list_of_urls in lists_of_urls_list :
            responses = await self.spider.get_urls(iterator_of_urls=list_of_urls)
            await asyncio.sleep(self.sleep_time)

            for response in responses:

                self.requested_urls.add(response['requested_url'])
                self.found_urls.remove(response['requested_url'])

                if response['status'] is not None:
                    if response['raw_urls'] is not None:
                        processor = self.url_extractor(iterator_of_urls=response['raw_urls'], current_page_url=response['responsed_url'])
                        new_found_urls = await processor.process_found_urls()

                        # Todo create new urls in db.
                        self.found_urls.update(new_found_urls)
                        self.found_urls = self.found_urls.difference(self.requested_urls)
                        print(self.found_urls)
            if self.found_urls:
                await self.crawl()
            else:
                raise ValueError(f'last urls is empty: {self.found_urls}')

    async def fetch_urls(self):
        pass

    def filter_found_urls(self):
        pass

    def limited_urls_iterators(self, urls):
        """
        Generate List of url lists.
        """
        self.max_requests
        if len(urls) > self.max_requests:
            return [
                urls[x : x + self.max_requests] for x in range(0, len(urls), self.max_requests)
            ]
        else:
            return [urls, ]