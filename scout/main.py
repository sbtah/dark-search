from crawlers.logic.base_spider import BaseSpider
from crawlers.logic.sync_spider import SyncSpider
from crawlers.logic.async_spider import AsyncSpider
from parsers.url import URLExtractor
from parsers.html import HtmlExtractor
import asyncio
import re
from urllib.parse import urlsplit, urlparse, urljoin
import time
import httpx
from lxml.html import tostring


urls = [
    'http://blogvl7tjyjvsfthobttze52w36wwiz34hrfcmorgvdzb6hikucb7aqd.onion/',
    'http://mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion/',
    'http://7ukmkdtyxdkdivtjad57klqnd3kdsmq6tp45rrsxqnu76zzv3jvitlqd.onion/'
]
async def async_test():
    crawler = AsyncSpider(initial_url=urls[0])
    responses = await crawler.get_urls(iterator_of_urls=urls)
    for element in responses:
        print(element)


def sync_test():
    crawler = SyncSpider(initial_url=urls[0])
    genex = crawler.get_urls(urls)
    for element in genex:
        print(element)


if __name__ == '__main__':
    # sync_test()
    asyncio.run(async_test())
