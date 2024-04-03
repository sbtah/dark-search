import time
from random import choice

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models


def return_agents():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
    ]
    return agents


class UserAgents(models.Model):
    """
    Class for storing and managing User Agents.
    """

    agents = ArrayField(
        models.TextField(max_length=2000), default=return_agents
    )
    last_update = models.IntegerField(default=0)

    @property
    def get_agent(self):
        return choice(self.agents)

    def save(self, *args, **kwargs):
        self.last_update = int(time.time())
        if not self.pk and UserAgents.objects.exists():
            # if you'll not check for self.pk
            # then error will also be raised in the update of exists model
            raise ValidationError('There is can be only one JuicerBaseSettings instance')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return 'Current User-Agents'
