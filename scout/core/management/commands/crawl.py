from django.core.management.base import BaseCommand
import asyncio
from logic.spiders.crawling_spider import Crawler
from libraries.adapters.task import TaskAdapter
from tasks.models import Task



url = 'http://darknet47w5otuw7koxrqgasuljjh6dhz7dw5iapmsekhjqbwipfpsad.onion/'
domain = 'darknet47w5otuw7koxrqgasuljjh6dhz7dw5iapmsekhjqbwipfpsad.onion'


class SomeShitName:

    def __init__(self, *args, **kwargs):
        self.task_adapter = TaskAdapter()
        self.crawler = Crawler

    def prepare_task(self):
        task = self.task_adapter.get_free_task()
        return task

    def start(self):
        """"""
        task = self.task_adapter.get_free_task()
        self.task_adapter.mark_task(task)
        crawler = self.crawler(crawl_type=task.type, initial_url=task.owner.url, initial_domain=task.owner.value)
        asyncio.run(crawler.crawl())
        self.task_adapter.unmark_task(task)

# async def crawler_test(initial_url, initial_domain):
#     # url_response = await TorScoutApiClient().get_not_crawled_website()
#     # if url_response is not None:

#     crawler = Crawler(crawl_type='SEARCH', initial_url=initial_url, initial_domain=initial_domain)
#     await crawler.crawl()



class Command(BaseCommand):
    '''Base command for restarting Celery workers.'''

    def handle(self, *args, **kwargs):

        SomeShitName().start()