import time
from random import choice
from typing import List
from urllib.parse import urlsplit

from logic.options.settings import USER_AGENTS
from utilities.logging import logger


class BaseSpider:
    """
    Base class for all crawlers.
    """

    def __init__(self, proxy='socks5://tor-privoxy:9050'):
        # Url of page that we requested initially.
        # This is for grouping of urls to: internal/external
        self._domain = None
        self.proxy = proxy
        self.start_time = int(time.time())
        self.end_time = None
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

    @property
    def domain(self):
        if self._domain is None and self._initial_url is not None:
            try:
                self._domain = urlsplit(self._initial_url).netloc
                return self._domain
            except Exception as e:
                raise e
        else:
            return None

    async def run(self):
        """
        Entrypoint for starting a spider.
        """
        raise NotImplementedError
