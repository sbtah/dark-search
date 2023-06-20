from search.crawlers.logic.base_crawler import BaseCrawler
import asyncio
import re
from urllib.parse import urlsplit, urlparse
import re


urls = ["http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion",]
proxy = 'socks5://127.0.0.1:9050'
proxy_2 = 'http://tor-privoxy:9050'
# http://comp-api:8000/api/users/token/


# def is_url(url):
#     try:
#         result = urlparse(url)
#         return all([result.scheme, result.netloc])
#     except ValueError:
#         return False


# crawler = BaseCrawler(proxy=proxy, start_url=urls[0])
# responses_iterator = asyncio.run(crawler.async_get_urls(iterator_of_urls=urls))
# for res in responses_iterator:
#     print(res)
#     parser = crawler.parser(response_text=res.text)
#     element = parser.generate_html_element()
#     if element:
#         a_tags = parser.find_all_elements(html_element=element, xpath_to_search='.//a[@href and not(@href="")]')
#         for tag in a_tags:
#             raw_url = tag.get('href')
#             if is_url(raw_url):
#                 print(raw_url)
#             else:
#                 print(f'THIS IS BAD: {raw_url}')




from search.scrapers.logic.base_scraper import BaseSeleniumScraper
from search.scrapers.logic.meta_scraper import MetaSeleniumScraper


with BaseSeleniumScraper() as scraper:
    scraper.selenium_get(url="http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion")