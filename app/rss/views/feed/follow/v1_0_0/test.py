from accounts.models import User, Token
from django.test import TestCase, Client
from rss.models import RSSFeed, RSSFeedFollow


class FollowTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/feed/follow/'
        self.user = User.objects.create(email='email')
        self.token = Token.objects.create(user=self.user)
        self.feed = RSSFeed.objects.create(url="feed_url")

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

    def test_already_followed(self):
        RSSFeedFollow.objects.create(user=self.user, feed=self.feed)

        body = {
            'pk': self.feed.pk
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['message'], "Feed already followed.")
