import time

from crawled.models.entity import Entity
from crawled.models.tag import Tag
from django.db import models


class Domain(models.Model):
    """
    Object representing a single unique TOR Domain.
    A Domain has many Webpages.
    """
    parent_entity = models.ForeignKey(
        Entity, on_delete=models.SET_NULL, blank=True, null=True
    )
    value = models.CharField(max_length=2000, unique=True, db_index=True)
    # Some entities host the same site on multiple different domains.
    # Saving 'favicon' images in base64 will help in identifying these cases.
    favicon_base64 = models.TextField(blank=True, null=True, db_index=True)
    server = models.CharField(max_length=100, blank=True, null=True)
    last_crawl_date = models.IntegerField(default=0)
    # This value increment on a crawl start.
    number_of_crawls = models.IntegerField(default=0)
    # This value increment on a crawl end.
    number_of_successful_crawls = models.IntegerField(default=0)
    # Calculated from the number of incoming links.
    average_crawl_time = models.IntegerField(default=0)
    domain_rank = models.FloatField(blank=True, null=True)
    # What is this Domain about.
    tags = models.ManyToManyField(Tag)
    site_structure = models.JSONField(blank=True, null=True)
    # Domains that this domain is linking to.
    linking_to = models.ManyToManyField('self', related_name='_linking_from', symmetrical=False)
    # A simple timeseries implementation of outbound links over time.
    # Where key will be a timestamp and value will be a list of domains.
    linking_to_logs = models.JSONField(blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'domains'
        db_table_comment = 'Found Tor domains. Domain has many Webpages.'

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.value

    @property
    def num_of_linking_to_domains(self):
        """
        Return number of current number of Domains that this Domain is linking to.
        """
        return int(self.linking_to.count())

    @property
    def num_of_linking_from_domains(self):
        """
        Return number of links that this Domain is receiving from all other Domains.
        """
        return int(self._linking_from.count())

    @property
    def linking_from(self):
        """
        Return Queryset of all Domains that this Domain is receiving links from.
        """
        return self._linking_from.all()
