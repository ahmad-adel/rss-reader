from django.db import models
from rss.models import RSSFeed


class RSSPost(models.Model):
    feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    guid = models.CharField(max_length=255, db_index=True)
    updated = models.DateTimeField()

    class Meta:
        verbose_name = 'RSS Post'
        verbose_name_plural = 'RSS Posts'
