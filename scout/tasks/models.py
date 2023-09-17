from django.db import models
from domains.models import Domain


class Task(models.Model):

    class Type(models.TextChoices):
        domain = 'DOMAIN'

    owner = models.OneToOneField(Domain, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.domain,
    )
    importance = models.IntegerField(default=0)
    number_of_launches = models.IntegerField(default=0)
    last_crawl_start = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.type}: {self.owner}'
