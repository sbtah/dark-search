import time

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Tag(models.Model):

    value = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.value


class Entity(models.Model):
    """
    Class representing TOR entity object.
    Entity can own many Domains.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Domain(models.Model):
    """Class for domain objects."""

    parent_entity = models.ForeignKey(
        Entity, on_delete=models.SET_NULL, blank=True, null=True
    )
    value = models.CharField(max_length=2000, unique=True)
    created = models.IntegerField(blank=True, null=True)
    last_crawl_date = models.IntegerField(blank=True, null=True)
    average_crawl_time = models.IntegerField(blank=True, null=True)
    server = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # New:
    number_of_crawls_finished = models.IntegerField(default=0)
    number_of_pages_found = models.IntegerField(default=0)

    description_tags = models.ManyToManyField(Tag)
    site_structure = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.value


class Webpage(models.Model):
    """Class for Webpage objects."""

    parent_domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

    url = models.URLField(max_length=2000, unique=True)
    # Since we could get redirected.
    url_after_request = models.URLField(max_length=2000)
    last_http_status = models.CharField(max_length=3, blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    raw_html = models.TextField(blank=True, null=True)
    page_title = models.CharField(max_length=2000, blank=True, null=True)
    meta_title = models.CharField(max_length=2000, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    on_page_raw_urls = ArrayField(models.URLField(
        max_length=2000),
        null=True,
        blank=True,
    )
    on_page_processed_urls = ArrayField(models.URLField(
        max_length=2000),
        null=True,
        blank=True,
    )
    # How many times we successfully requested this url?
    number_of_successful_requests = models.IntegerField(blank=True, null=True)
    number_of_unsuccessful_requests = models.IntegerField(
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False)
    created = models.IntegerField(blank=True, null=True)
    last_visit = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = int(time.time())
        super().save(*args, **kwargs)


    def __str__(self):
        return self.url
