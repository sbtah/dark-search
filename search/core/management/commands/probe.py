from django.core.management.base import BaseCommand
from logic.adapters.agents import UserAgentAdapter
from logic.adapters.url import UrlAdapter
from logic.objects.url import Url
from logic.spiders.synchronous import SyncSpider
from logic.spiders.probe import Probe



wiki_url_str = 'http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page' # noqa


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        agent = UserAgentAdapter().get_random_user_agent()
        proxy = 'http://search-privoxy:8118'
        wiki_url: Url = UrlAdapter.create_url_object(value=wiki_url_str)
        probe = SyncSpider(
            initial_url=wiki_url, proxy=proxy, user_agent=agent.value
        )
        res = probe.get(wiki_url)
        print(res[0].request)
