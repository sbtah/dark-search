import asyncio
import time
import traceback
from datetime import datetime

from logic.adapters.agents import UserAgentAdapter
from logic.adapters.proxy import ProxyAdapter
from logic.adapters.task import CrawlTaskAdapter
from logic.adapters.url import UrlAdapter
from logic.launchers.base import BaseLauncher
from logic.parsers.objects.url import Url
from logic.spiders.crawler import Crawler
from tasks.models import CrawlTask


class CrawlLauncher(BaseLauncher):
    """
    Launcher for crawlers.
    Fetch tasks from database,
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
    def now_timestamp() -> int:
        """Return integer from current timestamp."""
        return int(time.time())

    def launch(self, celery_task_id: str) -> None:
        """
        Prepare Proxy, UserAgent and CrawlTask.
        Launch crawling for task's domain.
        """
        # Starting timer and fetching active CrawlTask from db.
        time_start: int = self.now_timestamp()
        task: CrawlTask = self.crawl_task_adapter.get_and_prepare_crawling_task(
            celery_id=celery_task_id, launch_timestamp=time_start
        )
        self.logger.info(
            f'Launcher, launching task: task_id="{task.id}", domain="{task.domain}", '
            f'started="{datetime.fromtimestamp(time_start)}"'
        )

        # Fetching UserAgent and Proxy from db.
        user_agent: str = self.agent_adapter.get_random_user_agent().value
        proxy: str = self.proxy_adapter.get_proxy().value

        # Preparing Url object.
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
            time_end: int = self.now_timestamp()
            self.crawl_task_adapter.mark_task_finished(
                task=task, finished_timestamp=time_end, crawl_time_seconds=crawl_time
            )
            self.logger.info(
                f'Launcher, finished task: task_id="{task.id}", domain="{task.domain}", '
                f'finished="{datetime.fromtimestamp(time_end)}", crawl_time="{crawl_time}"'
            )
        except Exception as exc:
            time_end: int = self.now_timestamp()
            self.logger.error(
                f'Launcher, task failed: task_id="{task.id}", domain="{task.domain}", '
                f'failed_at="{datetime.fromtimestamp(time_end)}", error="{exc.__class__}", '
                f'error_message="{traceback.print_exception(exc)}"'
            )
            self.crawl_task_adapter.mark_task_failed(task=task)
