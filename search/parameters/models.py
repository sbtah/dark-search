from django.db import models


class UserAgent(models.Model):
    """
    Class for storing and managing User Agents.
    """

    class Type(models.TextChoices):
        chrome = 'CHROME'
        firefox = 'FIREFOX'

    type: models.CharField = models.CharField(max_length=10, choices=Type.choices, default=Type.firefox)
    value: models.CharField = models.CharField(max_length=255, unique=True, blank=False, default=None)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user-agents'
        db_table_comment = 'User Agents for many browsers.'
        verbose_name_plural = 'UserAgents'

    def __str__(self) -> str:
        return f'{self.type}:{self.value}:{self.created_at}'


class Proxy(models.Model):
    """
    Class representing the Proxy object.
    """

    class Type(models.TextChoices):
        dev = 'DEV'
        production = 'PRODUCTION'

    class Status(models.TextChoices):
        active = 'ACTIVE'
        disabled = 'DISABLED'

    value: models.CharField = models.CharField(max_length=255, unique=True)
    proxy_type: models.CharField = models.CharField(max_length=10, choices=Type.choices, default=Type.dev)
    status: models.CharField = models.CharField(max_length=10, choices=Status.choices, default=Status.active)
    current_spiders: models.IntegerField = models.IntegerField(default=0)

    class Meta:
        db_table = 'proxies'
        db_table_comment = 'Proxies information.'
        verbose_name_plural = 'Proxies'

    def __str__(self) -> str:
        return f'{self.proxy_type}:{self.value}:{self.status}'
