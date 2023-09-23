import asyncio
from logic.launchers.base import BaseLauncher
from tasks.models import Task
from domains.models import Domain

class CrawlerLauncher(BaseLauncher):
    """
    Utility for launching crawling for picked up Task.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def launch(self, task_id=None):
        """
        Launch Crawler for a Task.
        """

        # For testing.
        # domain = Domain.objects.get(value='vvedndyt433kopnhv6vejxnut54y5752vpxshjaqmj7ftwiu6quiv2ad.onion')
        # task = Task.objects.get(owner=domain)

        task = self.task_adapter.get_active_task()
        
        if task:
            self.logger.info(f"""
                    Launching crawling for Task: 
                        - {task.owner}
                """)
            task = self.task_adapter.mark_task_taken(task, task_id=task_id)
            crawler = self.crawler(initial_url=task.owner.url, initial_domain=task.owner.value)
            asyncio.run(crawler.start_crawling())
            task = self.task_adapter.mark_task_finished(task)
            self.logger.info(f"""
                                Finished crawling Task: 
                                    - {task.owner}
                            """)
