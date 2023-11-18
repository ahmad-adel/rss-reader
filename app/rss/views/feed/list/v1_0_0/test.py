from accounts.models import User, Token
from django.test import TestCase, Client
from rss.models import RSSFeed, RSSFeedFollow


class ListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/feed/list/'
        self.user = User.objects.create(email='email')
        self.token = Token.objects.create(user=self.user)
        self.feed = RSSFeed.objects.create(url="feed_url")
        self.feed_follow = RSSFeedFollow.objects.create(
            user=self.user, feed=self.feed)

    def test_success(self):
        response = self.client.get(
            self.url,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['feeds']), 1)
        self.assertEqual(data['feeds'][0]["is_followed"], True)
