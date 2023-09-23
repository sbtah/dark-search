from django.core.management.base import BaseCommand
from client.api import TorScoutApiClient
from logic.adapters.domain import DomainAdapter
from logic.adapters.task import TaskAdapter
from logic.organizers.organizer import TaskOrganizer
from tasks.models import Task
import time


DOMAINS = [
    'tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion',
    'hiddenmxictmv5wa4ljofvqiuskfjkxah2gvdpxxwbdmenufchlmooad.onion',
]


def prepare_launch():
    """"""
    for domain in DOMAINS:
        domain_object = DomainAdapter().sget_or_create_domain(domain=domain)
        task_object = TaskAdapter().sget_or_create_task(domain=domain_object)


class Command(BaseCommand):
    """"""

    def handle(self, *args, **kwargs):
        """"""
        
        self.stdout.write(self.style.SUCCESS(
            """
            Waiting for API to accept connections...
            """
        ))
        api = False

        while api is False:
            try:
                response = TorScoutApiClient().ping_home()
                if response:
                    if response.status_code == 200:
                        api = True
                else:
                    time.sleep(3)
            except Exception:
                self.stderr.write(self.style.ERROR(
                    """
                    API not Available, waiting...
                    """
                ))
                time.sleep(3)
        else:
            self.stderr.write(self.style.SUCCESS(
                """
                API is Available!
                """
            ))

        prepare_launch()
        tasks = Task.objects.all().count()
        taken = TaskAdapter().get_taken_tasks()
        if taken:
            TaskOrganizer().process_taken_tasks()
        self.stderr.write(self.style.SUCCESS(
                f"""
                Current number of Tasks in database: {tasks}
                """
            ))