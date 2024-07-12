from django.core.management.base import BaseCommand
from logic.client.base import BaseApiClient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        BaseApiClient()
