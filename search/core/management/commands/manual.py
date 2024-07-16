import asyncio

from django.core.management.base import BaseCommand
from logic.parsers.objects.url import Url
from logic.spiders.crawler import Crawler

# Url to crawl.
str_url = 'http://wiki6dtqpuvwtc5hopuj33eeavwa6sik7sy57cor35chkx5nrbmmolqd.onion' # noqa


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        agent = 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0' # noqa
        proxy = 'http://search-privoxy:8118'
        _url = Url(value=str_url)
        crawler = Crawler(
            initial_url=_url,
            proxy=proxy,
            user_agent=agent,
            urls_to_crawl=[_url, ],
            max_requests=5,
            sleep_time=0
        )
        asyncio.run(crawler.start_crawling())
