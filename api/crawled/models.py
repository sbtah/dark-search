from django.db import models
import time


class Website(models.Model):
    """Class for Website objects."""

    domain = models.URLField(max_length=200, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)
    # If all pages are inactive.
    is_active = models.BooleanField(default=False)
    website_map = models.JSONField()

    def save(self, *args, **kwargs):
        self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.domain

class Webpage(models.Model):
    """Class for Webpage objects."""

    parrent_website = models.ForeignKey(Website, on_delete=models.CASCADE)
    url = models.URLField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)
    number_of_references = models.IntegerField(blank=True, null=True)
    last_found = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url