import os
import time
from random import choice
from typing import List

from client.api import TorScoutApiClient
from dotenv import load_dotenv
from logic.adapters.domain import DomainAdapter
from logic.adapters.task import TaskAdapter
from logic.options.settings import USER_AGENTS
from logic.parsers.url import URLExtractor
from utilities.logging import logger


# Load .env file values.
load_dotenv()


class BaseSpider:
    """
    Base class for all crawlers.
    """

    def __init__(self, initial_url, initial_domain, proxy=os.environ.get('PROXY')):
        self.initial_url = initial_url
        self.initial_domain = initial_domain
        self.proxy = proxy
        self.client = TorScoutApiClient()
        self.domain_adapter = DomainAdapter()
        self.task_adapter = TaskAdapter()
        self.url_extractor = URLExtractor(current_page_url=initial_url)
        self.found_internal_urls = set()
        self.external_domains = set()
        self.requested_urls = set()
        self.crawl_start = int(time.time())
        self.crawl_end = None
        self.max_requests = 10
        self.sleep_time = 10
        self.site_structure = {}
        self.logger = logger

    @property
    def user_agent(self) -> str:
        agent = self.get_random_user_agent(USER_AGENTS)
        return agent

    @staticmethod
    def get_random_user_agent(user_agent_list: List[str]) -> str:
        """
        Returns str with random User-Agent.
        - :arg user_agent_list: List of strings with User Agents.
        """
        agent = choice(user_agent_list)
        return agent

    @staticmethod
    def now_timestamp():
        """
        Returns integer from current timestamp.
        """
        return int(time.time())

    # TODO:
    # Prepare proper header to mimic browser.
    def prepare_headers(self):
        pass
