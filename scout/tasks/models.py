from django.db import models
from domains.models import Domain


class Task(models.Model):

    class Type(models.TextChoices):
        domain = 'DOMAIN'

    class Status(models.TextChoices):
        active = 'ACTIVE'
        taken = 'TAKEN'
        finished = 'FINISHED'

    # If frequency is 1, then Task will be set to ACTIVE each day.
    # Task can only be set to ACTIVE if current status is FINISHED.
    class Frequency(models.IntegerChoices):
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
        six = 6
        seven = 7

    owner = models.OneToOneField(Domain, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.domain,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.active,
    )
    frequency = models.IntegerField(
        choices=Frequency.choices,
        default=Frequency.one,
    )
    importance = models.IntegerField(default=0)
    number_of_launches = models.IntegerField(default=0)
    number_of_finished_launches = models.IntegerField(default=0)
    # This is set on TAKEN status.
    last_launch_date = models.IntegerField(default=0)
    # This is set on FINISHED status.
    last_finished_launch_date = models.IntegerField(default=0)
    average_time_to_crawl = models.IntegerField(default=0)
    task_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.type}: {self.owner}'
