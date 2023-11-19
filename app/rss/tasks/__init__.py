from rss_reader.celery import app as celery_app

__all__ = ('celery_app',)

from .rss_feed_refresh import rss_feed_refresh_task
