from typing import Any

from django.db.models import QuerySet
from logic.adapters.base import BaseAdapter
from logic.exceptions.adapters.task import (
    NoActiveTasksError,
    NoTaskValueProvidedError,
)
from tasks.models import CrawlTask
from datetime import date


class CrawlTaskAdapter(BaseAdapter):
    """Adapter for interacting with CrawlTasks objects."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.task = CrawlTask
        super().__init__(*args, **kwargs)

    @staticmethod
    def calculate_average_time_to_finish(*, task: CrawlTask, crawl_time_seconds: int) -> int:
        """Helper method for calculating average time to finish field."""
        if task.average_time_to_finish is None:
            return crawl_time_seconds

        current_average: int = task.average_time_to_finish
        new_average: int = int((current_average + crawl_time_seconds) / task.number_of_finished_launches)
        return new_average

    def mark_task_active(self, *, task: CrawlTask) -> bool:
        """
        Set CrawlTask status to ACTIVE.
        - :arg task: CrawlTask object.
        """
        task.status = 'ACTIVE'
        task.current_celery_id = None
        task.save()
        self.logger.debug(f'TaskAdapter, marked task: status="ACTIVE", task_id="{task.id}"')
        return True

    def mark_task_taken(
        self,
        *,
        task: CrawlTask,
        for_launch: bool = True,
        celery_id: str | None = None,
        launch_date: date | None = None,
    ) -> bool:
        """
        Set CrawlTask status to 'TAKEN'.
        - :arg task: CrawlTask object.
        - :arg for_launch:
            Bool representing condition to save some additional values on Task,
            while setting status to 'TAKEN'. Defaults to True.
            If set to False only the status of a task will be updated.
        - :arg celery_id: String with ID of Celery Task.
        - :arg launch_date: Date object with date of launch.
        """
        message = f'TaskAdapter, marked task: status="TAKEN", task_id="{task.id}"'
        task.status = 'TAKEN'
        if for_launch is False:
            task.save()
            self.logger.debug(message)
            return True

        if for_launch is True and celery_id is None:
            raise NoTaskValueProvidedError()

        if for_launch is True and launch_date is None:
            raise NoTaskValueProvidedError()

        task.current_celery_id = celery_id
        task.last_launch_date = launch_date
        task.number_of_launches += 1
        task.save()
        self.logger.debug(message)
        return True

    def mark_task_failed(self, *, task: CrawlTask) -> bool:
        """
        Set CrawlTask status to FAILED.
        - :arg task: CrawlTask object.
        """
        task.status = 'FAILED'
        task.save()
        self.logger.debug(f'TaskAdapter, marked task: status="FAILED", task_id="{task.id}"')
        return True

    def mark_task_finished(
        self,
        *,
        task: CrawlTask,
        after_launch: bool = True,
        finished_date: date | None = None,
        crawl_time_seconds: int | None = None,
    ) -> bool:
        """
        Set CrawlTask status to 'FINISHED'.
        - :arg task: CrawlTask object.
        - :arg after_launch:
            Bool representing condition to save some additional values on Task,
            while setting status to 'FINISHED'. Defaults to True.
            If set to False only the status of the task will be updated.
        - :arg finished_date: Date object representing date when the task was finished.
        - :arg crawl_time_seconds: An integer representing the number of seconds it took to complete this task.
        """
        message = f'TaskAdapter, marked task: status="FINISHED", task_id="{task.id}"'
        task.status = 'FINISHED'

        if after_launch is False:
            task.save()
            self.logger.debug(message)
            return True

        if after_launch is True and finished_date is None:
            raise NoTaskValueProvidedError()

        if after_launch is True and crawl_time_seconds is None:
            raise NoTaskValueProvidedError()

        task.last_finished_date = finished_date
        task.number_of_finished_launches += 1
        average_time_to_finish: int = self.calculate_average_time_to_finish(
            task=task, crawl_time_seconds=crawl_time_seconds
        )
        task.average_time_to_finish = average_time_to_finish
        task.current_celery_id = None
        task.save()
        self.logger.debug(message)
        return True

    def _get_active_tasks(self) -> QuerySet[CrawlTask]:
        """
        Get the first ACTIVE Task object for crawling.
        Tasks are filtered by last_launch_date ASC and importance DESC.
        """
        tasks: QuerySet[CrawlTask] = self.task.objects.filter(
            status='ACTIVE', current_celery_id=None,
        ).order_by('last_launch_date', '-importance')
        return tasks

    def get_and_prepare_crawling_task(
        self,
        *,
        celery_id: str,
        launch_date: date,
    ) -> CrawlTask:
        """
        Start logic for launching CrawlTasks.
        Filter database for 'ACTIVE' CrawlTasks.
        Return first task from ordered queryset which is marked as 'TAKEN'.
        - :arg celery_id: String representing ID of Celery Task.
        - :arg launch_date: Date object representing date when the task was launched.
        """
        tasks: QuerySet[CrawlTask] = self._get_active_tasks()
        if len(tasks) == 0:
            raise NoActiveTasksError()

        task: CrawlTask = tasks.first()
        self.mark_task_taken(task=task, celery_id=celery_id, launch_date=launch_date)
        self.logger.info(
            f'TaskAdapter, prepared task: task_id="{task.id}", celery_id="{task.current_celery_id}", '
            f'domain="{task.domain}"'
        )
        return task

    async def async_get_or_create_task(self, domain: str) -> CrawlTask:
        """
        Try to create a new Task object or return existing one.
        Return the Task object.
        - :arg domain: String with domain value.
        """
        try:
            existing_task: CrawlTask = await self.task.objects.aget(domain=domain)
            self.logger.info(f'TaskAdapter, found existing Task: task_id="{existing_task.id}", domain="{domain}"')
            return existing_task
        except CrawlTask.DoesNotExist:
            new_task: CrawlTask = await self.task.objects.acreate(domain=domain)
            self.logger.info(f'TaskAdapter, created new Task: task_id="{new_task.id}", domain="{domain}"')
            return new_task

    def sync_get_or_create_task(self, domain: str) -> CrawlTask:
        """
        Create a new CrawlTask object or return existing one.
        Return the Task object.
        - :arg domain: String with domain value.
        """
        try:
            existing_task: CrawlTask = self.task.objects.get(domain=domain)
            self.logger.debug(f'TaskAdapter, found existing Task: task_id="{existing_task.id}", domain="{domain}"')
            return existing_task
        except CrawlTask.DoesNotExist:
            new_task: CrawlTask = self.task.objects.create(domain=domain)
            self.logger.debug(f'TaskAdapter, created new Task: task_id="{new_task.id}", domain="{domain}"')
            return new_task
