import time

from libraries.adapters.base import BaseAdapter
from tasks.models import Task


class TaskAdapter(BaseAdapter):
    """
    Simple adapter to help fetching and interacting with Task objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = Task

    def get_task_by_id(self, task_id: int):
        try:
            task_object = Task.objects.get(id=task_id)
            return task_object
        except Task.DoesNotExist:
            raise

    def get_free_task(self):
        task = Task.objects.all().order_by('number_of_launches').first()
        return task.id

    def mark_task(self, task_object: Task):
        task_object.number_of_launches += 1
        task_object.last_crawl_start = int(time.time())
        task_object.save()
        return task_object
