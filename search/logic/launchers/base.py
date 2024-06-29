"""
Base logic for launching Crawling or Probing of domains.
"""
from logic.adapters.url import UrlAdapter
from utilities.logging import logger


class BaseLauncher:
    """
    Base class for all Launchers.
    """

    def __init__(self):
        self.logger = logger
        self.url_adapter = UrlAdapter()

