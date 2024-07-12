# from django.core.management.base import BaseCommand
# from logic.adapters.agents import UserAgentAdapter
# from logic.adapters.url import UrlAdapter
# from logic.parsers.objects.url import Url
# from logic.spiders.synchronous import SyncSpider
#
# tor_66_url_str = 'http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion' # noqa
# wiki_url_str = 'http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/index.php/Main_Page' # noqa
#
#
# class Command(BaseCommand):
#
#     def handle(self, *args, **kwargs):
#         # crawler = BaseSpider(initial_url=full_url)
#         # This will be in launcher.
#         # PROXY = "socks5://search-privoxy:9050"
#         agent = UserAgentAdapter().get_random_user_agent()
#         # print(agent)
#         # proxy = ProxyAdapter().get_proxy()
#         # print(proxy)
#         proxy = 'http://search-privoxy:8118'
#
#         tor_url: Url = UrlAdapter.create_url_object(value=tor_66_url_str)
#         wiki_url: Url = UrlAdapter.create_url_object(value=wiki_url_str)
#         probe = SyncSpider(
#             initial_url=wiki_url, proxy=proxy, user_agent=agent.value
#         )
#         value = probe.request()
