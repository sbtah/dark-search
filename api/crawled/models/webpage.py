import time

from crawled.models.domain import Domain
from crawled.models.tag import Tag
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q, UniqueConstraint


class Webpage(models.Model):
    """
    Object representing a single Webpage(url) found while crawling TOR Domain.
    """
    parent_domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    url = models.URLField(max_length=2000, unique=True, db_index=True)
    is_homepage = models.BooleanField(default=False)
    # Since we could get redirected. This url does not have to be unique.
    url_after_request = models.URLField(max_length=2000)
    last_request_date = models.IntegerField(default=0)
    last_successful_request_date = models.IntegerField(default=0)
    last_http_status = models.CharField(max_length=3, blank=True, null=True)
    # Calculated for successful responses.
    average_response_time = models.FloatField(default=0)
    number_of_requests = models.IntegerField(default=0)
    number_of_successful_requests = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created = models.IntegerField(blank=True, null=True)

    # What is this Webpage about.
    tags = models.ManyToManyField(Tag)
    # How many times we successfully requested this url? status 200.
    detected_language = models.CharField(max_length=100, blank=True, null=True)
    # List of texts that the other sites are using in links.
    anchor_texts = ArrayField(models.CharField(max_length=2000), null=True, blank=True)
    # AI model will process this.
    translated_anchor_texts = ArrayField(models.CharField(max_length=2000), null=True, blank=True)

    class Meta:
        db_table = 'webpages'
        db_table_comment = 'Webpages found while crawling a Tor domain.'
        constraints = [
            UniqueConstraint(
                fields=['is_homepage'], condition=Q(is_homepage=True), name='There can be only one homepage.'
            ),
        ]

    def save(self, *args, **kwargs):
        if self.created is None:
            self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url


class Data(models.Model):
    """
    Object representing data saved from requesting a single Webpage.
    """
    webpage = models.OneToOneField(Webpage, on_delete=models.CASCADE)
    raw_text = models.TextField(blank=True, null=True)
    translated_text = models.TextField(blank=True, null=True)
    # h1 tag...
    page_title = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    meta_title = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    meta_description = models.TextField(blank=True, null=True, db_index=True)
    on_page_urls = ArrayField(models.URLField(max_length=2000), null=True, blank=True)
    on_page_processed_urls = ArrayField(models.URLField(max_length=2000), null=True, blank=True)

    class Meta:
        db_table = 'data'
        db_table_comment = 'Webpage data saved while crawling.'
        verbose_name_plural = 'Data'

    def __str__(self):
        return f'Data of: {self.webpage.url}'
