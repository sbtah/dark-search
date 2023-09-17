import asyncio

from celery import chain, shared_task


@shared_task(bind=True)
def request_task_to_work(self):
    """"""
    from libraries.adapters.task import TaskAdapter
    task_id = TaskAdapter().get_free_task()
    return task_id


@shared_task(bind=True)
def start_crawler_for_task(self, task_id):
    """"""
    from libraries.adapters.task import TaskAdapter
    from logic.spiders.crawling_spider import Crawler
    task_object = TaskAdapter().get_task_by_id(task_id=task_id)
    task_object = TaskAdapter().mark_task(task_object)
    crawler = Crawler(crawl_type=task_object.type, initial_url=task_object.owner.url, initial_domain=task_object.owner.value)
    asyncio.run(crawler.crawl())
    return task_object.id

@shared_task(
    bind=True, 
    autoretry_for=(Exception,),
    retry_backoff=60,
    ignore_result=True,
    retry_jitter=True,
    retry_kwargs={'max_retries': 2},)
def crawl(self):
    chain(request_task_to_work.s(), start_crawler_for_task.s()).apply_async()
