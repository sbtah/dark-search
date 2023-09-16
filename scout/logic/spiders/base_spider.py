from random import choice
from typing import List
import os
from client.api import TorScoutApiClient
from libraries.adapters.domain import DomainAdapter
from logic.options.settings import USER_AGENTS
from utilities.logging import logger
from dotenv import load_dotenv


load_dotenv()


class BaseSpider:
    """
    Base class for all crawlers.
    """

    def __init__(self, proxy=os.environ.get('PROXY')):
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

    async def crawl(self):
        """
        Entrypoint for starting a spider.
        """
        raise NotImplementedError
