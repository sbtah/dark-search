from django.core.management.base import BaseCommand
from logic.organizers.organizer import TaskOrganizer
from logic.adapters.task import TaskAdapter
from tasks.models import Task


class Command(BaseCommand):
    """Base command for restarting Celery workers."""

    def handle(self, *args, **kwargs):
        tasks_ids = TaskOrganizer().process_finished_tasks()

        # for task in tasks:
        #     print(task)
        #     db_task = Task.objects.filter(task_id=task.get('id'))
        #     print(db_task)

