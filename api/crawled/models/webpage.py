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
    url_after_request = models.URLField(max_length=2000)
    last_request_date = models.DateTimeField(blank=True, null=True)
    last_successful_request_date = models.DateTimeField(blank=True, null=True)
    last_http_status = models.CharField(max_length=3, blank=True, null=True)
    last_http_status_logs = models.JSONField(blank=True, null=True)
    average_response_time = models.FloatField(default=0)
    number_of_requests = models.IntegerField(default=0)
    number_of_successful_requests = models.IntegerField(default=0)
    page_rank = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    linking_to_webpages = models.ManyToManyField(
        'self', related_name='_linking_from_webpages', symmetrical=False,)
    linking_to_webpages_logs = models.JSONField(blank=True, null=True)
    anchor_texts = ArrayField(models.CharField(max_length=2000), null=True, blank=True)
    translated_anchor_texts = ArrayField(models.CharField(max_length=2000), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'webpages'
        db_table_comment = 'Webpages found while crawling a Tor domain.'
        constraints = [
            UniqueConstraint(
                fields=['is_homepage'], condition=Q(is_homepage=True), name='There can be only one homepage.'
            ),
        ]

    def __str__(self):
        return self.url

    @property
    def num_of_linking_to_webpages(self):
        """
        Return number of current number of Webpages that this Webpage is linking to.
        """
        return int(self.linking_to_webpages.count())

    @property
    def num_of_linking_from_webpages(self):
        """
        Return number of links that this Webpage is receiving from all other Webpages.
        """
        return int(self._linking_from_webpages.count())

    @property
    def linking_from_webpages(self):
        """
        Return Queryset of all Domains that this Domain is receiving links from.
        """
        return self._linking_from_webpages.all()


class Data(models.Model):
    """
    Object representing data saved from requesting a single Webpage.
    """
    webpage = models.OneToOneField(Webpage, on_delete=models.CASCADE)
    raw_text = models.TextField(blank=True, null=True)
    detected_language = models.CharField(max_length=100, blank=True, null=True)
    translated_text = models.TextField(blank=True, null=True)
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
        return f'Data of: {self.webpage}'
