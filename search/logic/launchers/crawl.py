from logic.adapters.task import CrawlTaskAdapter
from logic.launchers.base import BaseLauncher
from logic.spiders.crawler import Crawler


class CrawlLauncher(BaseLauncher):
    """
    Launcher of crawlers.
    """

    def __init__(self, *args, **kwargs):
        self.crawler = Crawler
        self.crawl_task_adapter = CrawlTaskAdapter()
        super().__init__(*args, **kwargs)

