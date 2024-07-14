from django.db import models


class Entity(models.Model):
    """
    Object representing organization or owner of TOR operation.
    Entity can own many Domains.
    """
    # Entity can own many domains, basically serving same or many different domains.
    name = models.CharField(max_length=255, unique=True, db_index=True)
    # Description for entity. Can be set manually or scraped from any source.
    description = models.TextField(blank=True, null=True)
    # Any data about entity like: contact info, bitcoin wallets, telegram or jabber channels, etc...
    additional_data = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'entities'
        db_table_comment = 'Entities owning domains.'
        verbose_name_plural = 'Entities'

    def __str__(self):
        return self.name
