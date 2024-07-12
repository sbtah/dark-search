import asyncio

from django.core.management.base import BaseCommand
from logic.client.base import BaseApiClient
from logic.client.asynchronous import AsyncApiClient


class Command(BaseCommand):
    """Base command for restarting Celery workers."""

    def handle(self, *args, **kwargs):

        client = BaseApiClient()
