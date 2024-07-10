from django.core.management.base import BaseCommand
from logic.launchers.crawl import CrawlLauncher


class Command(BaseCommand):
    """Base command for starting crawling manually."""

    def handle(self, *args, **kwargs):
        CrawlLauncher().launch(celery_task_id='MANUAL')
