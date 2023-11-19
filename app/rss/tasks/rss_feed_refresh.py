import celery

from django.utils import timezone
from django.db import transaction
from rss.models import RSSFeed
from utils.rss.rss_processor import RSSProcessor


@celery.shared_task
class RSSFeedRefreshTask(celery.Task):
    def run(self, *args, **kwargs):
        """Refresh the RSS feeds that should be refreshed.
        Feed is refreshed if next_fetch datetime has passed.
        select_for_update() is used to lock the feeds being updated
        to prevent other tasks from writing changes before this is done (task runs every minute)
        """
        processor = RSSProcessor()
        with transaction.atomic():
            feeds = RSSFeed.objects.filter(next_fetch__lte=timezone.now())\
                .exclude(next_fetch=None)\
                .select_for_update()

            for feed in feeds:
                processor.process_feed(feed)
