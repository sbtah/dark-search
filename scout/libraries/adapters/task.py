from libraries.adapters.base import BaseAdapter
from tasks.models import Task
from domains.models import Domain
import time

class TaskAdapter(BaseAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = Task

    def get_free_task(self):
        task_object = Task.objects.filter(status='IDLE').order_by('-last_run').first()
        return task_object

    def mark_task(self, task_object):
        task_object.status = 'RUNNING'
        task_object.save()

    def unmark_task(self, task_object):
        task_object.status = 'IDLE'
        task_object.last_run = int(time.time())
        task_object.save()