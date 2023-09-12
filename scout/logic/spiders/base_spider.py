import time
from random import choice
from typing import List

from client.api import TorScoutApiClient
from libraries.adapters.domain import DomainAdapter
from libraries.adapters.task import TaskAdapter
from logic.options.settings import USER_AGENTS
from utilities.logging import logger


class BaseSpider:
    """
    Base class for all crawlers.
    """

    def __init__(self, proxy='socks5://tor-privoxy:9050'):
        self.proxy = proxy
        self.client = TorScoutApiClient()
        self.domain_adapter = DomainAdapter()
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

    async def run(self):
        """
        Entrypoint for starting a spider.
        """
        raise NotImplementedError
