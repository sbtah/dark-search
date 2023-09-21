import asyncio
import time

from django.core.management.base import BaseCommand
from logic.adapters.task import TaskAdapter
from logic.spiders.crawling_spider import Crawler


class CrawlerLauncher:
    """
    Object representing simple Celery task logic.
    """

    def __init__(self, *args, **kwargs):
        self.task_adapter = TaskAdapter()
        self.crawler = Crawler

    def start(self):
        """
        Entry for each task object.
        Simply grab 1st free Task in database and run crawler for its owner.
        """
        task = self.task_adapter.get_active_task()
        print(task)
        if task:
            task = self.task_adapter.mark_task_taken(task)
            crawler = self.crawler(initial_url=task.owner.url, initial_domain=task.owner.value)
            try:
                print(crawler)
                asyncio.run(crawler.start_crawling())
                task = self.task_adapter.mark_task_finished(task)
            except Exception as e:
                print(f'EXCEPTION: {e}')


class Command(BaseCommand):
    """Base command for restarting Celery workers."""

    def handle(self, *args, **kwargs):
        CrawlerLauncher().start()
