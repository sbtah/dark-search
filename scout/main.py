from logic.crawlers.spiders.base_spider import BaseSpider
from logic.crawlers.spiders.sync_spider import SyncSpider
from logic.crawlers.spiders.async_spider import AsyncSpider
from logic.parsers.url import URLExtractor
from logic.parsers.html import HtmlExtractor
import asyncio
import re
from urllib.parse import urlsplit, urlparse, urljoin
import time
import httpx
from lxml.html import tostring


urls = [
    'http://blogvl7tjyjvsfthobttze52w36wwiz34hrfcmorgvdzb6hikucb7aqd.onion/',
    'http://mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion/',
    'http://7ukmkdtyxdkdivtjad57klqnd3kdsmq6tp45rrsxqnu76zzv3jvitlqd.onion/',
]
async def async_test():
    crawler = AsyncSpider(initial_url=urls[0])
    responses = await crawler.get_urls(iterator_of_urls=urls)
    return responses


def sync_test():
    crawler = SyncSpider(initial_url=urls[0])
    genex = crawler.get_urls(urls)
    for element in genex:

        crawler.search_for_urls(response=element)


if __name__ == '__main__':
    #sync_test()
    out = asyncio.run(async_test())
    print(out)