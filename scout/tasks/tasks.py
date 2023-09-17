from celery import shared_task
from django.db import transaction
import asyncio
import time
from celery import chain
# from libraries.adapters.task import TaskAdapter
# from logic.spiders.crawling_spider import Crawler



# class CrawlingTask:
#     """
#     Object representing simple Celery task logic.
#     """

#     def __init__(self, *args, **kwargs):
#         self.task_adapter = TaskAdapter()
#         self.crawler = Crawler
#         self.start_time = int(time.time())
#         self.end_time = None

#     def get_task(self):
#         task = self.task_adapter.get_free_task()
#         if task is None:
#             raise ValueError('No Task found. Initial Task must be created manually.')
#         return task

#     def mark_task(self, task):
#         task = self.task_adapter.mark_task(task=task)
#         return task

#     def start_crawling(self, task):
#         crawler = self.crawler(crawl_type=task.type, initial_url=task.owner.url, initial_domain=task.owner.value)
#         try:
#             asyncio.run(crawler.crawl())
#         except Exception as e:
#             self.logger.error(f'Task Errror: {e}')
#             pass
#         finally:
#             self.end_time = int(time.time())
#             return task
    

    # def start(self):
    #     """
    #     Entry for each task object.
    #     Simply grab 1st free Task from database and run crawler for its owner.
    #     """
    #     task = self.task_adapter.get_free_task()
    #     if task is None:
    #         raise ValueError('No Task found. Initial Task must be created manually.')
    #     self.task_adapter.mark_task(task)
    #     crawler = self.crawler(crawl_type=task.type, initial_url=task.owner.url, initial_domain=task.owner.value)
    #     try:
    #         asyncio.run(crawler.crawl())
    #         self.end_time = int(time.time())
    #         run_seconds = self.end_time - self.start_time
    #         self.task_adapter.successful_unmark_task(task_object=task, crawl_time=run_seconds)
    #     except Exception as e:
    #         self.end_time = int(time.time())
    #         run_seconds = self.end_time - self.start_time
   #         self.task_adapter.unsuccessful_unmark_task(task_object=task, crawl_time=run_seconds, error_message=e)


#### 
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


@shared_task(bind=True)
def crawl(self):
    chain(request_task_to_work.s(), start_crawler_for_task.s()).apply_async()

#####
# @shared_task(
#         bind=True,
#         autoretry_for=(Exception,),
#         retry_backoff=60,
#         ignore_result=True,
#         retry_jitter=True,
#         retry_kwargs={'max_retries': 2},
# )
# def crawl(self):
#     """
#     Basic crawl Task.
#     """
#     start_time = int(time.time())

#     task = TaskAdapter().get_free_task()
#     if task is None:
#         raise ValueError('No Task found. Initial Task must be created manually.')
    
#     TaskAdapter().mark_task(task)
#     crawler = Crawler(
#         crawl_type=task.type,
#         initial_url=task.owner.url,
#         initial_domain=task.owner.value
#     )
#     try:
#         asyncio.run(crawler.crawl())
#         end_time = int(time.time())
#         run_seconds = end_time - start_time
#         TaskAdapter().successful_unmark_task(task_object=task, crawl_time=run_seconds)
#     except Exception as e:
#         end_time = int(time.time())
#         run_seconds = end_time - start_time
#         TaskAdapter().unsuccessful_unmark_task(task_object=task, crawl_time=run_seconds, error_message=e)