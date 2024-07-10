from django.core.management.base import BaseCommand
from logic.adapters.agents import UserAgentAdapter
from logic.adapters.proxy import ProxyAdapter
from logic.adapters.task import CrawlTaskAdapter
from django.contrib.auth import get_user_model


# Hardcoded values:
DOMAINS = [
    'zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion',
    'tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion'
]

AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Mozilla/5.0 (X11; Linux i686; rv:128.0) Gecko/20100101 Firefox/128.0',
]

PROXIES = [
    'http://search-privoxy:8118',
]


def prepare_initial_tasks() -> None:
    """Prepare starting domains."""
    for domain in DOMAINS:
        CrawlTaskAdapter().sync_get_or_create_task(domain=domain)


def prepare_initial_user_agents() -> None:
    """Prepare starting User Agents."""
    for agent in AGENTS:
        UserAgentAdapter().sync_get_or_create_user_agent(user_agent=agent)


def prepare_initial_proxy() -> None:
    for proxy in PROXIES:
        ProxyAdapter().sync_get_or_create_proxy(proxy=proxy)


def prepare_super_user() -> None:
    user = get_user_model()  # get the currently active user model,
    if not user.objects.filter(username='admin').exists():
        user.objects.create_superuser('admin', 'admin@example.com', 'admin')


class Command(BaseCommand):
    """
    Prepare command logic.
    """

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("""Preparing SEARCH service initial objects...""")
        )
        prepare_initial_tasks()
        prepare_initial_proxy()
        prepare_initial_user_agents()
        prepare_super_user()
        self.stdout.write(
            self.style.SUCCESS("""SEARCH service initial objects ready !""")
        )
