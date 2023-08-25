from crawlers.logic.base import BaseCrawler
from parsers.url_parser import BaseURLParser
from parsers.html_parser import BaseHTMLParser
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


# async def async_get(client: httpx.AsyncClient, url: str) -> str:
#     """
#     Requests specified URL asynchronously. Returns JSON.
#     - :arg client: Asynchronous client.
#     - :arg url: Requested URL.
#     """
#     try:
#         res = await client.get(url)
#         return res
#     except Exception as e:
#         return None

# async def get_urls(urls_iterator):
#     async with httpx.AsyncClient(proxies='socks5://127.0.0.1:9050') as client:
#         tasks = []
#         for url in urls_iterator:
#             tasks.append(
#                 asyncio.create_task(
#                     async_get(client=client, url=url)
#                 )
#             )
#         resps = await asyncio.gather(*tasks)
#         return resps

async def test_x():
    crawler = BaseCrawler()
    resps = await crawler.async_get_urls(iterator_of_urls=urls)
    for res in resps:
        print(type(res))
        print(crawler.page(res))

if __name__ == '__main__':
    # outs = asyncio.run(get_urls(urls))
    # print(outs)
    resps = asyncio.run(test_x())


    # async def get_products_by_ids(
    #     self,
    #     range_of_product_ids: Iterator[int],
    #     single_product_by_id_url: str,
    # ) -> Future[Dict]:
    #     """
    #     Sends requests to SINGLE_PRODUCT_BY_ID asynchronously.
    #     - :arg range_of_product_ids: Iterator of integers (IDs)
    #         that will be used while sending requests.
    #     - :arg single_product_by_id_url: API Url for Product Endopoint.
    #     """
    #     async with httpx.AsyncClient() as client:
    #         tasks = []
    #         for num in range_of_product_ids:
    #             tasks.append(
    #                 asyncio.ensure_future(
    #                     self.async_get(
    #                         client,
    #                         single_product_by_id_url.format(num),
    #                     )
    #                 )
    #             )
    #         products = await asyncio.gather(*tasks)
    #         return products