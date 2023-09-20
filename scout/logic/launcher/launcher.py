import asyncio
from logic.adapters.task import TaskAdapter
from logic.spiders.crawling_spider import Crawler


class CrawlerLauncher:

    def __init__(self, *args, **kwargs):
        self.task_adapter = TaskAdapter()
        self.crawler = Crawler

    def launch(self, task_id=None):
        """
        Launch Crawler for Task.
        """
        task = self.task_adapter.get_active_task()
        if task:
            task = self.task_adapter.mark_task_taken(task, task_id=task_id)
            crawler = self.crawler(initial_url=task.owner.url, initial_domain=task.owner.value)
            asyncio.run(crawler.start_crawling())
            task = self.task_adapter.mark_task_finished(task)
