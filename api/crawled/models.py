import time

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Tag(models.Model):
    """
    Class representing Tag object.
    Tags will be used as classifications for Domains.
    """
    value = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = "tags"
        db_table_comment = "Classification tags for domains and webpages."

    def __str__(self):
        return self.value


class Entity(models.Model):
    """
    Object representing organization or owner of TOR operation.
    Entity can own many Domains.
    """
    # Entity can own many domains, basically serving same or many different domains.
    name = models.CharField(max_length=255, unique=True, db_index=True)
    # Description for entity, can be set manually or scraped from any source.
    description = models.TextField(blank=True, null=True)
    # Any data about entity like: contact info, bitcoin wallets, telegram or jabber channels etc...
    additional_data = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "entities"
        db_table_comment = "Entities owning domains."
        verbose_name_plural = 'Entities'

    def __str__(self):
        return self.name


class Domain(models.Model):
    """
    Object representing a single unique TOR Domain.
    A Domain has many Webpages.
    """
    parent_entity = models.ForeignKey(
        Entity, on_delete=models.SET_NULL, blank=True, null=True
    )
    value = models.CharField(max_length=2000, unique=True, db_index=True)
    server = models.CharField(max_length=100, blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)
    last_crawl_date = models.IntegerField(default=0)
    average_crawl_time = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    additional_data = models.JSONField(blank=True, null=True)
    # Will increment on crawl start.
    number_of_crawls = models.IntegerField(default=0)
    # Will increment on crawl end.
    number_of_successful_crawls = models.IntegerField(default=0)
    # What is this Domain about.
    description_tags = models.ManyToManyField(Tag)
    site_structure = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "domains"
        db_table_comment = "Found Tor domains. Domain has many Webpages."

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.value


class Webpage(models.Model):
    """
    Object representing a single Webpage(url) found while crawling TOR Domain.
    """
    parent_domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    url = models.URLField(max_length=2000, unique=True, db_index=True)
    # Since we could get redirected. This url does not have to be unique.
    url_after_request = models.URLField(max_length=2000)
    last_request_date = models.IntegerField(default=0)
    last_http_status = models.CharField(max_length=3, blank=True, null=True)
    # Calculated for successful responses.
    average_response_time = models.FloatField(default=0)
    html = models.TextField(blank=True, null=True)
    # h1 tag...
    page_title = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    meta_title = models.CharField(max_length=2000, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True, db_index=True)
    additional_data = models.JSONField(blank=True, null=True)
    # What is this Webpage about.
    description_tags = models.ManyToManyField(Tag)
    # Raw urls found.
    on_page_urls = ArrayField(models.URLField(max_length=2000), null=True, blank=True)
    on_page_processed_urls = ArrayField(models.URLField(max_length=2000), null=True, blank=True)
    # How many times we successfully requested this url? status 200.
    number_of_successful_requests = models.IntegerField(default=0)
    number_of_unsuccessful_requests = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created = models.IntegerField(blank=True, null=True)

    # Ideas for identifiers:
    # - Head hash
    # - base64 favicon - on domain ?

    class Meta:
        db_table = "webpages"
        db_table_comment = "Webpages found while crawling a Tor domain."

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url
