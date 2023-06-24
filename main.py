from search.crawlers.logic.base import BaseCrawler
import asyncio
import re
from urllib.parse import urlsplit, urlparse, urljoin
import re


urls = ["http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion",]
proxy = 'socks5://127.0.0.1:9050'
proxy_2 = 'http://tor-privoxy:9050'
# http://comp-api:8000/api/users/token/





# crawler = BaseCrawler(proxy=proxy, start_url=urls[0])
# responses_iterator = asyncio.run(crawler.async_get_urls(iterator_of_urls=urls))
# for res in responses_iterator:
#     print(res)
#     html = crawler.html(response_text=res.text)
#     element = html.generate_html_element()
#     if element is not None:
#         a_tags = html.find_all_elements(html_element=element, xpath_to_search='.//a[@href and not(@href="")]')
#         for tag in a_tags:
#             raw_url = tag.get('href')
#             url = crawler.url(url=raw_url)
#             if url.is_valid_url(url=raw_url):
#                 print(raw_url)
#             else:
#                 print(f'THIS IS BAD: {raw_url}')
#                 print(f'Fixed: {urljoin(crawler.start_url, raw_url)}')


crawler = BaseCrawler(proxy=proxy, start_url=urls[0])
res = crawler.get(url=crawler.start_url)

html_parser = crawler.html_parser(response_text=res.text)
url_parser = crawler.url_parser(url=urls[0], start_domain=urls[0])

html_element = html_parser.generate_html_element()

if html_element is not None:
    a_tags = html_parser.find_all_elements(html_element=html_element, xpath_to_search='.//a[@href and not(@href="")]')

    for tag in a_tags:

        raw_url = tag.get('href')
        if url_parser.is_valid_url(url=raw_url):
            print(raw_url)
        else:
            fixed = url_parser.fix_url(url=raw_url)
            if fixed is not None:
                print(fixed)
            else:
                print(raw_url)


        # if url.is_valid_url(url=raw_url):
        #     print(raw_url)
        # else:
        #     print(f'THIS IS BAD: {raw_url}')
        #     print(f'Fixed: {urljoin(crawler.start_url, raw_url)}')


# from search.scrapers.logic.base_scraper import BaseSeleniumScraper
# from search.scrapers.logic.meta_scraper import MetaSeleniumScraper


# with BaseSeleniumScraper() as scraper:
#     scraper.selenium_get(url="http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion")