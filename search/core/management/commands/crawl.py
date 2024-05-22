import asyncio
import time
from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from logic.spiders.crawler import Crawler
from logic.spiders.base import BaseSpider
from tasks.models import CrawlTask
from logic.adapters.agents import UserAgentAdapter
from logic.adapters.proxy import ProxyAdapter


domain = 'tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion'
full_url = f'http://{domain}/'


class Command(BaseCommand):
    """Base command for restarting Celery workers."""

    def handle(self, *args, **kwargs):
        # crawler = BaseSpider(initial_url=full_url)
        # This will be in launcher.
        agent = UserAgentAdapter().get_random_user_agent()
        proxy = ProxyAdapter().get_proxy()
        crawler = Crawler(initial_url=full_url, proxy=proxy.value, user_agent=agent.value, urls_to_crawl=[full_url, ], max_requests=5, sleep_time=2)

        print(crawler.proxy)
        asyncio.run(crawler.start_crawling())