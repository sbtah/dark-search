from django.db import models


class Domain(models.Model):

    value = models.CharField(max_length=3000, unique=True)
    url = models.URLField(max_length=3000, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.url is None:
            self.url = f'http://{self.value}'
        super().save(*args, **kwargs)


    def __str__(self):
        return self.value
