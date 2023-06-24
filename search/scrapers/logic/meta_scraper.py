from typing import Callable, Dict, Iterator, List, Union

from lxml.html import HtmlElement
from selenium.webdriver.remote.webelement import WebElement

from search.scrapers.logic.base import BaseSeleniumScraper


class MetaSeleniumScraper(BaseSeleniumScraper):
    """
    Scraper that specifies in requesting and scraping Webpage meta data.
    """

    def __init__(self, requested_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requested_url = requested_url


    def visit_page(self, url: str) -> HtmlElement:
        """
        Entrypoint for all scraping logic.
        Visits requested page by url.
        Since we don't store session or cookies,
        each time with have to close cookies banner.
        Returns HtmlElement generated after banner was closed.
        """
        try:
            request = self.selenium_get(url=url)
            if request is not None:
                element = self.generate_html_element()
                self.close_cookies_banner(html_element=element)
                after_element = self.generate_html_element()
                return after_element
            else:
                self.logger.error('Failed at requesting page URL.')
                raise ValueError
        except Exception as e:
            self.logger.error(f'(visit_page) Some other Exception: {e}')
            raise


    def extract_head_element(self, html_element, xpath_to_search, name, property, content, rel, href, description, src, title, text, type):
        pass