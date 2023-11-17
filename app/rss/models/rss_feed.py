from django.db import models
from django.utils import timezone


class RSSFeed(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    failure_counter = models.IntegerField(default=0)
    updated = models.DateTimeField(null=True)
    last_fetch = models.DateTimeField(null=True)
    next_fetch = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self):
        return self.title
    
    def set_updated(self, updated):
        self.updated = updated
        self.save()

    def update_fetch_times(self, last_fetch, next_fetch):
        self.last_fetch = last_fetch
        self.next_fetch = next_fetch
        self.save()

    class Meta:
        verbose_name = 'RSS Feed'
        verbose_name_plural = 'RSS Feeds'
