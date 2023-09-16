from django.db import models
from domains.models import Domain


class Task(models.Model):

    class Type(models.TextChoices):
        domain = 'DOMAIN'

    class Status(models.TextChoices):
        idle = 'IDLE'
        running = 'RUNNING'

    owner = models.OneToOneField(Domain, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.domain,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.idle,
    )
    # AKA priority
    # TODO:
    # Change to choice field 0 to 9.
    importance = models.IntegerField(default=1)
    number_of_runs = models.IntegerField(default=0)
    last_crawl_time = models.IntegerField(default=0)
    average_time_to_crawl = models.IntegerField(blank=True, null=True)
    last_run = models.IntegerField(blank=True, null=True)
    last_error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.type}: {self.owner}'
