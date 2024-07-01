import asyncio
import time
from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from logic.spiders.crawler import Crawler
from logic.spiders.base import BaseSpider
from tasks.models import CrawlTask
from logic.adapters.agents import UserAgentAdapter
from logic.adapters.proxy import ProxyAdapter
from logic.parsers.objects.url import Url


domain = 'tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion'
full_url = f'http://{domain}/'
new_url = 'http://s4k4ceiapwwgcm3mkb6e4diqecpo7kvdnfr5gg7sph7jjppqkvwwqtyd.onion/'
ex_url = 'http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page'

class Command(BaseCommand):
    """Base command for restarting Celery workers."""

    def handle(self, *args, **kwargs):
        # crawler = BaseSpider(initial_url=full_url)
        # This will be in launcher.
        # PROXY = "socks5://search-privoxy:9050"
        # agent = UserAgentAdapter().get_random_user_agent()
        # print(agent)
        # proxy = ProxyAdapter().get_proxy()
        # print(proxy)
        agent = 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
        proxy = 'http://search-privoxy:8118'

        url_tor_66 = Url(value=full_url)
        wiki_url = Url(value=ex_url)
        crawler = Crawler(
            initial_url=wiki_url,
            proxy=proxy,
            user_agent=agent,
            urls_to_crawl=[wiki_url, ],
            max_requests=5,
            sleep_time=0
        )
        asyncio.run(crawler.start_crawling())
