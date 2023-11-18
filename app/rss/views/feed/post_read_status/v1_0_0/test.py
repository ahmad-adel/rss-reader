from requests import post
from accounts.models import User, Token
from django.test import TestCase, Client
from rss.models import RSSFeed, RSSFeedFollow, RSSPost, RSSPostRead


class PostReadStatusTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/feed/post-read-status/'
        self.user = User.objects.create(email='email')
        self.token = Token.objects.create(user=self.user)
        self.feed = RSSFeed.objects.create(url="feed_url")
        self.post = RSSPost.objects.create(feed=self.feed, guid="1")

    def test_success_read(self):
        body = {
            'pk': self.post.pk,
            'is_read': True
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        read_posts = RSSPostRead.objects.all()
        self.assertEqual(read_posts.count(), 1)

    def test_success_unread(self):
        RSSPostRead.objects.create(user=self.user, post=self.post)
        body = {
            'pk': self.post.pk,
            'is_read': False
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        read_posts = RSSPostRead.objects.all()
        self.assertEqual(read_posts.count(), 0)
