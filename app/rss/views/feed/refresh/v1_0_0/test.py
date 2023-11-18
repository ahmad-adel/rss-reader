from accounts.models import User, Token
from django.test import TestCase, Client
from utils.rss.rss_processor import RSSProcessor
from rss.models import RSSFeed


class RefreshTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/feed/refresh/'
        self.user = User.objects.create(email='email')
        self.token = Token.objects.create(user=self.user)
        self.feed = RSSFeed.objects.create(url="feed_url")

        RSSProcessor.process_feed = lambda self, feed: None       # mock RSSProcessor

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
