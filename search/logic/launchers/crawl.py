import asyncio
from datetime import date, datetime

from logic.adapters.agents import UserAgentAdapter
from logic.adapters.proxy import ProxyAdapter
from logic.adapters.task import CrawlTaskAdapter
from logic.adapters.url import UrlAdapter
from logic.launchers.base import BaseLauncher
from logic.objects.url import Url
from logic.spiders.crawler import Crawler
from tasks.models import CrawlTask
from django.conf import settings


class CrawlLauncher(BaseLauncher):
    """
    Launcher for crawlers.
    Fetch tasks from the database,
    mark them with proper status,
    launch crawling for task.domain.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.crawler = Crawler
        self.proxy_adapter: ProxyAdapter = ProxyAdapter()
        self.agent_adapter: UserAgentAdapter = UserAgentAdapter()
        self.crawl_task_adapter: CrawlTaskAdapter = CrawlTaskAdapter()
        self.url_adapter: UrlAdapter = UrlAdapter()
        super().__init__(*args, **kwargs)

    @staticmethod
    def now_date() -> date:
        """Return integer from current timestamp."""
        return datetime.now()

    def launch(self, celery_task_id: str) -> None:
        """
        Prepare Proxy, UserAgent and CrawlTask.
        Launch crawling for task's domain.
        """
        # Setting time_start date and fetching active CrawlTask from db.
        time_start: date = self.now_date()
        task: CrawlTask = self.crawl_task_adapter.get_and_prepare_crawling_task(
            celery_id=celery_task_id, launch_date=time_start
        )
        self.logger.info(
            f'Launcher, launching task: task_id="{task.id}", domain="{task.domain}", '
            f'started="{time_start.strftime(settings.PROJECT_DATE_FORMAT)}"'
        )

        # Fetching UserAgent and Proxy from db.
        user_agent: str = self.agent_adapter.get_random_user_agent().value
        proxy: str = self.proxy_adapter.get_proxy().value

        # Preparing the Url object.
        prepared_url: str = f'http://{task.domain}'
        url: Url = self.url_adapter.create_url_object(value=prepared_url)

        try:
            # Prepare a crawler instance.
            crawler = Crawler(
                initial_url=url,
                proxy=proxy,
                user_agent=user_agent,
                urls_to_crawl=[url, ],
                max_requests=5,
                sleep_time=0
            )

            result: dict = asyncio.run(crawler.start_crawling())
            crawl_time: int = result['time']
            time_end: date = self.now_date()
            self.crawl_task_adapter.mark_task_finished(
                task=task, finished_date=time_end, crawl_time_seconds=crawl_time
            )
            self.logger.info(
                f'Launcher, finished task: task_id="{task.id}", domain="{task.domain}", '
                f'finished="{time_end.strftime(settings.PROJECT_DATE_FORMAT)}", '
                f'crawl_time="{crawl_time}"'
            )
        except Exception as exc:
            time_end: date = self.now_date()
            self.logger.error(
                f'Launcher, task failed: task_id="{task.id}", domain="{task.domain}", '
                f'failed_at="{time_end.strftime(settings.PROJECT_DATE_FORMAT)}", '
                f'error="{exc.__class__}", '
                f'message="{exc}"', exc_info=True
            )
            self.crawl_task_adapter.mark_task_failed(task=task)
