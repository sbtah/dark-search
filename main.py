from search.crawlers.logic.base import BaseCrawler
from search.parsers.url_parser import BaseURLParser
import asyncio
import re
from urllib.parse import urlsplit, urlparse, urljoin
import re

test_url = 'http://bbzzzsvqcrqtki6umym6itiixfhni37ybtt7mkbjyxn2pgllzxf2qgyd.onion/?referrer=14977&utm_source=tor_66&utm_medium=banner&utm_campaign=tor66_jun23#Bangbag'
urls = ["http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion",]
proxy = 'socks5://127.0.0.1:9050'
proxy_2 = 'http://tor-privoxy:9050'



# parser = BaseURLParser(current_page_url=urls[0])

# test_url_2 = '/advertise/?referrer=14977&utm_source=tor_66&utm_medium=banner&utm_campaign=tor66_jun23#Bangbag'
# print(parser.clean_url(url=test_url_2))

async def tester():
    crawler = BaseCrawler(proxy=proxy, start_url=urls[0])
    responses_iterator = await crawler.async_get_urls(iterator_of_urls=urls)
    for res in responses_iterator:
        urls_found = await crawler.search_for_urls(response_text=res.text)
        for u in urls_found:
            print(u)


# crawler = BaseCrawler(proxy=proxy, start_url=urls[0])
# res = crawler.get(url=crawler.start_url)
#
# html_parser = crawler.html_parser(response_text=res.text)
# url_parser = crawler.url_parser(current_page_url=urls[0])
#
# html_element = html_parser.generate_html_element()
#
# if html_element is not None:
#     a_tags = html_parser.find_all_elements(html_element=html_element, xpath_to_search='.//a[@href and not(@href="")]')
#
#     for tag in a_tags:
#         raw_url = tag.get('href')
#         print(url_parser.process_found_url(url=raw_url))


# from search.scrapers.logic.base_scraper import BaseSeleniumScraper
# from search.scrapers.logic.meta_scraper import MetaSeleniumScraper


# with BaseSeleniumScraper() as scraper:
#     scraper.selenium_get(url="http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion")


if __name__ == '__main__':
    asyncio.run(tester())