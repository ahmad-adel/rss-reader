import celery


class RSSFeedRefreshTask(celery.Task):
    def run(self, *args, **kwargs):
        pass