from django.db import models


class RSSFeed(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    failure_counter = models.IntegerField()
    last_update = models.DateTimeField(null=True)
    next_update = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'RSS Feed'
        verbose_name_plural = 'RSS Feeds'
