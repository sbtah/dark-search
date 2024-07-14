from django.db import models


class Tag(models.Model):
    """
    Class representing the Tag object.
    Tags will be used as classifications for Domains.
    """
    value = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = "tags"
        db_table_comment = "Classification tags for domains and webpages."

    def __str__(self):
        return self.value
