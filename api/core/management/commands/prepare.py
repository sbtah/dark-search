from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


def prepare_super_user() -> None:
    user = get_user_model()  # get the currently active user model,
    if not user.objects.filter(username='admin').exists():
        user.objects.create_superuser('admin', 'admin@example.com', 'admin')


class Command(BaseCommand):
    """
    Prepare command logic.
    """

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("""Preparing API service initial objects...""")
        )
        prepare_super_user()
        self.stdout.write(
            self.style.SUCCESS("""API service initial objects ready !""")
        )
