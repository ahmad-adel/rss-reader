from django.db import models


class RSSFeed(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    failure_counter = models.IntegerField()
    updated = models.DateTimeField(null=True)
    last_fetch = models.DateTimeField(null=True)
    next_fetch = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'RSS Feed'
        verbose_name_plural = 'RSS Feeds'
