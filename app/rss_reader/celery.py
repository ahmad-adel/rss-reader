from __future__ import absolute_import
from celery import Celery
from rss_reader.settings import INSTALLED_APPS


app = Celery('rss_reader')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: INSTALLED_APPS)
