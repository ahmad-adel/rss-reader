import datetime
import mongomock
import feedparser

from django.test import TestCase
from django.utils import timezone
from rss.models import RSSFeed, RSSPost
from utils.mongo.rss_post_manager import RSSPostManager
from utils.rss.rss_fetcher import RSSFetcher
from utils.rss.rss_processor import RSSProcessor


# Mock MongoDB manager
MongoClient = mongomock.MongoClient
class MockRSSPostManager(RSSPostManager):
    def __init__(self) -> None:
        self.collection = mongomock.MongoClient().db.collection


class TestRSSProcessorView(TestCase):
    def setUp(self):
        self.feed = RSSFeed.objects.create(url="feed_url")
        self.feed_data = {
            "bozo": False,
            "status": 200,
            "feed": {
                "title": "title",
                "description": "description",
                "updated_parsed": [1990, 1, 1, 1, 1, 1, 0, 0, 0],
            },
            "entries": [
                {
                    "id": "post_id",
                    "published_parsed": [2023, 11, 17, 19, 52, 0, 4, 321, 0],
                    "field": "value",
                }
            ],
        }

        # Mock the mongo interface (in-memory mongo)
        self.rss_processor = RSSProcessor()
        self.rss_processor.RSSPostManagerInstance = MockRSSPostManager()

        # Mock RSS fetcher response
        def mock_rss_fetcher(url: str) -> dict:
            return self.feed_data
        feedparser.parse = mock_rss_fetcher

    def test_success(self):
        self.rss_processor.process_feed(self.feed)

        # Feed processed
        feed = RSSFeed.objects.get(pk=self.feed.pk)
        self.assertEqual(feed.title, "title")
        self.assertEqual(feed.description, "description")
        self.assertEqual(
            feed.updated,
            datetime.datetime(year=1990, month=1, day=1, hour=1, minute=1, second=1, tzinfo=timezone.utc)
        )
        self.assertNotEqual(feed.next_fetch, None)
        self.assertNotEqual(feed.last_fetch, None)
        self.assertEqual(feed.next_fetch, feed.last_fetch + datetime.timedelta(minutes=5))

        # Posts processed
        posts = RSSPost.objects.filter(feed=feed)
        self.assertEqual(posts.count(), 1)
        self.assertEqual(posts[0].guid, "post_id")
        self.assertEqual(
            posts[0].published,
            datetime.datetime(*self.feed_data["entries"][0]["published_parsed"][:6], tzinfo=timezone.utc)
        )
        self.assertEqual(
            self.rss_processor.RSSPostManagerInstance.fetch(posts[0].pk),
            self.feed_data["entries"][0]
        )

    def test_refresh_failed_first(self):
        self.feed_data["status"] = 0

        self.rss_processor.process_feed(self.feed)

        self.feed.refresh_from_db()
        self.assertEqual(self.feed.failure_counter, 1)
        self.assertEqual(self.feed.updated, None)
        self.assertEqual(self.feed.next_fetch, self.feed.last_fetch + datetime.timedelta(minutes=2))

    def test_refresh_failed_second(self):
        self.feed_data["status"] = 0
        self.feed.failure_counter = 1
        self.feed.save()

        self.rss_processor.process_feed(self.feed)

        self.feed.refresh_from_db()
        self.assertEqual(self.feed.failure_counter, 2)
        self.assertEqual(self.feed.updated, None)
        self.assertEqual(self.feed.next_fetch, self.feed.last_fetch + datetime.timedelta(minutes=5))

    def test_refresh_failed_third(self):
        self.feed_data["status"] = 0
        self.feed.failure_counter = 2
        self.feed.save()

        self.rss_processor.process_feed(self.feed)

        self.feed.refresh_from_db()
        self.assertEqual(self.feed.failure_counter, 3)
        self.assertEqual(self.feed.updated, None)
        self.assertEqual(self.feed.next_fetch, self.feed.last_fetch + datetime.timedelta(minutes=8))

    def test_refresh_failed_fourth(self):
        self.feed_data["status"] = 0
        self.feed.failure_counter = 3
        self.feed.save()

        self.rss_processor.process_feed(self.feed)

        self.feed.refresh_from_db()
        self.assertEqual(self.feed.failure_counter, 0)
        self.assertEqual(self.feed.updated, None)
        self.assertEqual(self.feed.next_fetch, None)


