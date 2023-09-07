from logic.spiders.base_spider import BaseSpider
from logic.spiders.sync_spider import SyncSpider
from logic.spiders.async_spider import AsyncSpider
from logic.parsers.url import URLExtractor
from logic.parsers.html import HtmlExtractor
import asyncio
import re
from urllib.parse import urlsplit, urlparse, urljoin
import time
import httpx
from lxml.html import tostring
from logic.crawlers.base import BaseCrawler


urls = {'http://mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion/',
        'http://omegalock5zxwbhswbisc42o2q2i54vdulyvtqqbudqousisjgc7j7yd.onion/',
        'http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/',
        'http://wiki6dtqpuvwtc5hopuj33eeavwa6sik7sy57cor35chkx5nrbmmolqd.onion/'}

test_urls = ['http://mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion/' for number in range(1000)]

# async def crawl_page(iterator_of_urls=None):
#     crawler = AsyncSpider()
#     responses = await crawler.get_urls(iterator_of_urls=iterator_of_urls)
#     for response in responses:
#         if response.get('raw_urls') is not None:
#             processor = URLExtractor(iterator_of_urls=response['raw_urls'], current_page_url=response['requested_url'])
#             processed_urls = await processor.process_found_urls()
#             print(processed_urls)
#             await crawl_page(iterator_of_urls=processed_urls)
#         # raw_urls = response.get('raw_urls')
#         # if raw_urls is not None:
#         #     # TODO:
#         #     # All list to set in one go
#         #     extractor = URLExtractor(iterator_of_urls=raw_urls)
#         #     processed = await extractor.process_found_urls()

async def crawler_test():
    crawl = BaseCrawler(urls)
    await crawl.crawl()

def sync_test():
    crawler = SyncSpider(initial_url=urls[0])
    genex = crawler.get_urls(urls)
    for element in genex:

        crawler.search_for_urls(response=element)


if __name__ == '__main__':
    #sync_test()
    # out = asyncio.run(crawl_page(iterator_of_urls=urls))
    asyncio.run(crawler_test())