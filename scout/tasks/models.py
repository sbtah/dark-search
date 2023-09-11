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
    importance = models.IntegerField(default=1)
    last_run = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.type}: {self.owner}'
