import re
from urllib.parse import urljoin, urlsplit
from lxml.html import HtmlElement
from utilities.logging import logger
from typing import List


class URLExtractor:

    def __init__(self, current_page_url):
        self.current_page_url = current_page_url
        self.logger = logger

    async def get_domain(self, url) -> str:
        """
        Extracts domain from parsed URL.
        :arg url: String with URL address to extract domain from.
        """
        try:
            domain = urlsplit(url).netloc
            return domain
        except Exception as e:
            self.logger.error(f'(get_domain) Some other exception: {e}')
            raise

    async def is_file(self, url):
        files_types = (
            '.zip',
            '.7z',
            '.rar',
            '.doc',
            '.docx',
            '.pdf',
            '.ods',
            '.xlsx',
            '.xls',
            '.ods',
            '.txt',
            '.odt',
            '.ods',
            '.tar.gz',
            '.tgz',
            '.tar.Z',
            '.tar.bz2',
            '.tbz2',
            '.tar.lz',
            '.tlz',
            '.tar.xz',
            '.txz',
            '.tar.zst',
            '.png',
            '.jpg',
            '.jpeg',
            '.png',
            '.csv',
        )
        try:
            path = urlsplit(url).path
            if path:
                for ftype in files_types:
                    if ftype in path:
                        return True
        except Exception as e:
            self.logger.error(f'(get_domain) Some other exception: {e}')
            raise

    async def clean_url(self, url: str) -> str:
        """
        Cleans URL of all query params or fragments.
        Returns cleaned URL.

        :arg url: String with URL address to clean.
        """
        try:
            result = urlsplit(url)
            if result.query or result.fragment:
                return urljoin(url, result.path)
            else:
                return url
        except Exception as e:
            self.logger.error(f'(clean_url) Some other Exception: {e}')
            raise

    async def fix_paths(self, url: str) -> str:
        """
        Fixes path URL by joining it with domain.
        Returns proper URL on success.

        :arg url: String with URL address to fix.
        """
        try:
            if self.current_page_url is not None:
                fixed_url = urljoin(self.current_page_url, url)
                if await self.is_valid_url(url=fixed_url):
                    return fixed_url
                else:
                    return url
        except Exception as e:
            self.logger.error(f'(fix_paths) Some other Exception: {e}')
            raise

    async def is_valid_url_parse(self, url: str) -> bool:
        """
        Validates URL by parsing it with urlsplit.

        :arg url: String with URL address to check.
        """
        try:
            result = urlsplit(url)
            return bool(result.scheme and result.netloc)
        except ValueError:
            return False

    async def is_onion(self, url: str) -> bool:
        """
        Checks if given URL address is an onion URL.
        Returns bool.

        :arg url: String with URL address to check.
        """
        if url is not None:
            try:
                domain = urlsplit(url).netloc
                if domain:
                    match = re.search(r'\S+\.onion$', domain)
                    if match:
                        return True
                    else:
                        return False
                else:
                    pass
            except Exception as e:
                self.logger.error(f'(is_onion) Some other Exception: {e}')
                raise
        else:
            pass

    async def is_valid_url_regex(self, url: str) -> bool:
        """
        Validates URL by Regex.

        :arg url: String with URL address to check.
        """
        try:
            pattern = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return bool(pattern.match(url))
        except Exception as e:
            self.logger.error(f'(is_valid_url_regex) Some other Exception: {e}')
            raise

    async def is_valid_url(self, url: str) -> bool:
        """
        Validates URL by parsing and Regex.
        Returns bool.

        :arg url: String with URL address to check.
        """
        if await self.is_valid_url_parse(url) is True and await self.is_valid_url_regex(url) is True:
            return True
        return False

    async def process_found_urls(self, iterator_of_urls=None):
        """
        Processes found URLS in many ways.
        First of all this method is cleaning URL of any query parameters and fragments.
        Then it tries to fix any paths by joining found urls with requested url.
        Lastly it checks validity of found URL and is URL an onion.
        """
        processed_urls = set()
        if iterator_of_urls is not None:
            for url in iterator_of_urls:
                cleaned = await self.clean_url(url=url.strip())
                if await self.is_valid_url(url=cleaned) and await self.is_onion(url=cleaned) and not await self.is_file(url=cleaned):
                    processed_urls.add(cleaned)
                else:
                    fixed = await self.fix_paths(url=cleaned)
                    if await self.is_onion(url=fixed) and await self.is_valid_url(url=fixed) and not await self.is_file(url=fixed):
                        processed_urls.add(fixed)
                    else:
                        continue
            return processed_urls
        else:
            return None
