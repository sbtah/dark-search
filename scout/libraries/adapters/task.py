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

    def calculate_average_time_to_crawl(self, task_object: Task, last_crawl_time: int):
        if task_object.average_time_to_crawl is not None:
            task_object.average_time_to_crawl = int((task_object.average_time_to_crawl + last_crawl_time) / (task_object.number_of_successful_runs if task_object.number_of_successful_runs != 0 else 1))
            return task_object
        else:
            task_object.average_time_to_crawl = last_crawl_time
            return task_object

    def get_free_task(self):
        task_object = Task.objects.filter(status='IDLE').order_by('-last_run').first()
        return task_object

    def mark_task(self, task_object: Task):
        task_object.status = 'RUNNING'
        task_object.save()

    def unsuccessful_unmark_task(self, task_object: Task, crawl_time, error_message: str = None):
        task_object.status = 'IDLE'
        task_object.last_run = int(time.time())
        task_object.number_of_runs += 1
        task_object.last_crawl_time = crawl_time if crawl_time is not None else 0
        if error_message is not None:
            task_object.last_error_message = error_message
        task_object.save()

    def successful_unmark_task(self, task_object: Task, crawl_time: int):
        task_object.status = 'IDLE'
        task_object.last_run = int(time.time())
        task_object.number_of_runs += 1
        task_object = self.calculate_average_time_to_crawl(task_object=task_object, last_crawl_time=crawl_time)
        task_object.last_crawl_time = crawl_time if crawl_time is not None else 0
        task_object.save()
