"""
Base logic for launching Crawling or Probing of domains.
"""
from logic.adapters.url import UrlAdapter
from utilities.log import logger


class BaseLauncher:
    """
    Base class for all Launchers.
    """

    def __init__(self) -> None:
        self.logger = logger
        self.url_adapter = UrlAdapter()
