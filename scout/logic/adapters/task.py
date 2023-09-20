import time

from logic.adapters.base import BaseAdapter
from tasks.models import Task
from domains.models import Domain
from django.db.models import QuerySet


class TaskAdapter(BaseAdapter):
    """
    Simple adapter to help fetching and interacting with Task objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = Task

    async def get_or_create_task(self, domain: Domain) -> Task:
        """
        Returns existing or creates Task object.
        - :arg domain: Domain object.
        """
        try:
            existing_task = await self.task.objects.aget(owner=domain)
            return existing_task
        except Task.DoesNotExist:
            new_task = await self.task.objects.acreate(owner=domain)
            return new_task

    def get_task_by_id(self, task_id: int):
        try:
            task_object = Task.objects.get(id=task_id)
            return task_object
        except Task.DoesNotExist:
            raise
        
    def get_active_task(self) -> Task:
        task = Task.objects.filter(status='ACTIVE').order_by('id', 'last_launch_date').first()
        return task

    def get_taken_tasks(self) -> QuerySet:
        tasks = Task.objects.filter(status='TAKEN')
        return tasks
    
    def get_finished_tasks(self) -> QuerySet:
        tasks = Task.objects.filter(status='FINISHED')
        return tasks
    
    def mark_task_active(self, task_object: Task):
        """"""
        task_object.status = 'ACTIVE'
        task_object.save()
        return task_object

    def mark_task_taken(self, task_object: Task, task_id=None):
        task_object.status = 'TAKEN'
        task_object.number_of_launches += 1
        task_object.last_launch_date = int(time.time())
        task_object.task_id = task_id
        task_object.save()
        return task_object
    
    def mark_task_finished(self, task_object: Task, task_id=None):
        task_object.status = 'FINISHED'
        task_object.number_of_finished_launches += 1
        task_object.last_finished_launch_date = int(time.time())

        if task_object.average_time_to_crawl == 0:
            task_object.average_time_to_crawl = (task_object.last_finished_launch_date - task_object.last_launch_date) / task_object.number_of_finished_launches
        else:
            task_object.average_time_to_crawl = (task_object.average_time_to_crawl + (task_object.last_finished_launch_date - task_object.last_launch_date)) / task_object.number_of_finished_launches
        task_object.task_id = None
        task_object.save()
        return task_object

