from django.core.management.base import BaseCommand
from logic.adapters.agents import UserAgentAdapter
from logic.adapters.proxy import ProxyAdapter
from logic.parsers.objects.url import Url
from logic.spiders.synchronous import SyncSpider

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
        agent = UserAgentAdapter().get_random_user_agent()
        # print(agent)
        # proxy = ProxyAdapter().get_proxy()
        # print(proxy)
        proxy = 'http://search-privoxy:8118'

        url_tor_66 = Url(value=full_url)
        probe = SyncSpider(initial_url=url_tor_66, proxy=proxy, user_agent=agent.value)
        value = probe.request(url_tor_66)
        print(value)