from django.conf import settings
from django.db import models
from rss.models import RSSPost


class RSSPostRead(models.Model):
    post = models.ForeignKey(RSSPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'RSS Post Read'
        verbose_name_plural = 'RSS Post Reads'
