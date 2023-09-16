from celery import shared_task

import asyncio
import time


from libraries.adapters.task import TaskAdapter
from logic.spiders.crawling_spider import Crawler


class CrawlingTask:
    """
    Object representing simple Celery task logic.
    """

    def __init__(self, *args, **kwargs):
        self.task_adapter = TaskAdapter()
        self.crawler = Crawler
        self.start_time = int(time.time())
        self.end_time = None

    def start(self):
        """
        Entry for each task object.
        Simply grab 1st free Task from database and run crawler for its owner.
        """
        task = self.task_adapter.get_free_task()
        if task is None:
            raise ValueError('No Task found. Initial Task must be created manually.')
        self.task_adapter.mark_task(task)
        crawler = self.crawler(crawl_type=task.type, initial_url=task.owner.url, initial_domain=task.owner.value)
        try:
            asyncio.run(crawler.crawl())
            self.end_time = int(time.time())
            run_seconds = self.end_time - self.start_time
            self.task_adapter.successful_unmark_task(task_object=task, crawl_time=run_seconds)
        except Exception as e:
            self.end_time = int(time.time())
            run_seconds = self.end_time - self.start_time
            self.task_adapter.unsuccessful_unmark_task(task_object=task, crawl_time=run_seconds, error_message=e)


@shared_task
def crawl():
    CrawlingTask().start()
