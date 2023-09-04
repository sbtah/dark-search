from django.db import models
import time


class Tag(models.Model):

    value = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.value


class Website(models.Model):
    """Class for Website objects."""

    domain = models.URLField(max_length=200, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)
    # website_map = models.JSONField(blank=True, null=True)
    description_tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.domain


class Webpage(models.Model):
    """Class for Url objects."""

    parent_website = models.ForeignKey(Website, on_delete=models.CASCADE)
    url = models.URLField(max_length=255, unique=True)
    created = models.IntegerField(blank=True, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_file = models.BooleanField(default=False)
    number_of_references = models.IntegerField(blank=True, null=True)
    last_visit = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.created = int(time.time())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url
