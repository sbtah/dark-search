from django.db import models


class CrawlTask(models.Model):
    """Base object for a crawl task."""

    domain: models.CharField = models.CharField(
        max_length=255, unique=True, blank=False, default=None, db_index=True
    )
    current_celery_id: models.CharField = models.CharField(max_length=100, blank=True, null=True)
    last_launch_date: models.DateTimeField = models.DateTimeField(
        db_index=True, blank=True, null=True
    )
    last_finished_date: models.DateTimeField = models.DateTimeField(
        db_index=True, blank=True, null=True
    )
    number_of_launches: models.IntegerField = models.IntegerField(default=0)
    number_of_finished_launches: models.IntegerField = models.IntegerField(default=0)
    average_time_to_finish: models.IntegerField = models.IntegerField(default=0)
    importance: models.IntegerField = models.IntegerField(default=0)

    class Status(models.TextChoices):
        active = 'ACTIVE'
        taken = 'TAKEN'
        failed = 'FAILED'
        finished = 'FINISHED'

    class Frequency(models.IntegerChoices):
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
        six = 6
        seven = 7

    status: models.CharField = models.CharField(max_length=10, choices=Status.choices, default=Status.active)
    frequency: models.IntegerField = models.IntegerField(choices=Frequency.choices, default=Frequency.one)

    class Meta:
        db_table = 'crawl_tasks'
        db_table_comment = 'Task data and statistics.'
        verbose_name_plural = 'CrawlTasks'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{str(self.domain)}'
