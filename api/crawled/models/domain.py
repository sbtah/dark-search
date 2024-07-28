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
    last_crawl_date = models.DateTimeField(blank=True, null=True)
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
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'domains'
        db_table_comment = 'Found Tor domains. Domain has many Webpages.'

    @property
    def num_of_webpages(self) -> int:
        """
        Return number of all children webpages for current Domain.
        """
        return self.webpage_set.count()

    def __str__(self):
        return self.value
