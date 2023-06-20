from lxml.html import HtmlElement, HTMLParser, fromstring
from typing import List, Union
from search.utilities.logging import logger
from urllib.parse import urlsplit, urlparse


class BaseURLParser:

    def __init__(self, url):
        self.url = url
