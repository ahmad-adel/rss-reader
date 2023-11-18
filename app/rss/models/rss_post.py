from django.db import models
from rss.models import RSSFeed


class RSSPost(models.Model):
    feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    guid = models.CharField(max_length=255, db_index=True)
    published = models.DateTimeField(null=True)

    def set_published(self, published):
        self.published = published
        self.save()

    class Meta:
        verbose_name = 'RSS Post'
        verbose_name_plural = 'RSS Posts'
        constraints = [
            models.UniqueConstraint(
                fields=['feed', 'guid'],
                name='feed_guid_unique',
            )
        ]
