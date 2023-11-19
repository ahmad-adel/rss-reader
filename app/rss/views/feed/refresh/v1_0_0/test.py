import feedparser

from accounts.models import User, Token
from django.test import TestCase, Client
from rss.models import RSSFeed


class RefreshTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/feed/refresh/'
        self.user = User.objects.create(email='email')
        self.token = Token.objects.create(user=self.user)
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

        # Mock RSS fetcher response
        def mock_rss_fetcher(url: str) -> dict:
            return self.feed_data
        feedparser.parse = mock_rss_fetcher

    def test_success(self):
        body = {
            'pk': self.feed.pk
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)

    def test_feed_not_found(self):
        body = {
            'pk': -1
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['message'], "Feed not found.")
