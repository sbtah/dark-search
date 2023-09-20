from random import choice
from typing import List
import os
from client.api import TorScoutApiClient
from logic.adapters.domain import DomainAdapter
from logic.adapters.task import TaskAdapter
from logic.options.settings import USER_AGENTS
from utilities.logging import logger
from dotenv import load_dotenv


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
        self.found_internal_urls = set()
        self.external_domains = set()
        self.requested_urls = set()
        self.max_requests = 10
        self.sleep_time = 10
        self.site_structure = {}
        self.logger = logger

    async def get_proxy(self):
        pass

    @staticmethod
    def get_random_user_agent(user_agent_list: List[str]) -> str:
        """
        Returns str with random User-Agent.
        - :arg user_agent_list: List of strings with User Agents.
        """
        agent = choice(user_agent_list)
        return agent

    @property
    def user_agent(self) -> str:
        agent = self.get_random_user_agent(USER_AGENTS)
        return agent

    # TODO:
    # Prepare proper header to mimic browser.
    async def prepare_headers(self):
        pass
