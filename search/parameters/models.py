import time
from django.db import models


# def return_agents():
#     agents = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
#         'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
#     ]
#     return agents


class UserAgent(models.Model):
    """
    Class for storing and managing User Agents.
    """

    class Type(models.TextChoices):
        chrome = 'CHROME'
        firefox = 'FIREFOX'

    type = models.CharField(max_length=10, choices=Type.choices, default=Type.firefox)
    value = models.CharField(max_length=255, unique=True, blank=False, default=None)
    created = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.type}:{self.value}:{self.created}'


class Proxy(models.Model):
    """
    Class representing Proxy object.
    """

    class Type(models.TextChoices):
        dev = 'DEV'
        production = 'PRODUCTION'

    class Status(models.TextChoices):
        active = 'ACTIVE'
        disabled = 'DISABLED'

    type = models.CharField(max_length=10, choices=Type.choices, default=Type.dev)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.active)
    value = models.CharField(max_length=255, unique=True, blank=False, default=None)
    current_spiders = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.type}:{self.value}:{self.status}'
