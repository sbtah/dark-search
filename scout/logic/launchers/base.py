from logic.adapters.task import TaskAdapter
from logic.spiders.crawling_spider import Crawler
from utilities.logging import logger


class BaseLauncher:
    """
    Base class for Launcher.
    """

    def __init__(self, *args, **kwargs):
        self.task_adapter = TaskAdapter()
        self.crawler = Crawler
        self.logger = logger
