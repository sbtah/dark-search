import asyncio
import time

from django.core.management.base import BaseCommand
from logic.adapters.task import TaskAdapter
from logic.spiders.crawling_spider import Crawler
from logic.launchers.launcher import CrawlerLauncher



class Command(BaseCommand):
    """Base command for restarting Celery workers."""

    def handle(self, *args, **kwargs):
        CrawlerLauncher().launch()
