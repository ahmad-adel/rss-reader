from django.conf import settings
from django.db import models
from rss.models import RSSFeed


class RSSFeedFollow(models.Model):
    post = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'RSS Feed Follow'
        verbose_name_plural = 'RSS Feed Follows'
