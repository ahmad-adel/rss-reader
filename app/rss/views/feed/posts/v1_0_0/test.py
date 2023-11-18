import mongomock

from accounts.models import User, Token
from django.test import TestCase, Client
from django.utils import timezone
from rss.models import RSSFeed, RSSFeedFollow, RSSPost, RSSPostRead
from utils.mongo.rss_post_manager import RSSPostManager


class PostsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/feed/posts/'
        self.user = User.objects.create(email='email')
        self.token = Token.objects.create(user=self.user)
        self.feed = RSSFeed.objects.create(url="feed_url")
        self.feed_2 = RSSFeed.objects.create(url="feed_url")

        for i in range(13):
            RSSPost.objects.create(
                feed=self.feed, guid=str(i), published=timezone.now())

        read_post = RSSPost.objects.first()
        RSSPostRead.objects.create(
            user=self.user, post=read_post)      # only one read post

        # no posts for followed feed
        RSSFeedFollow.objects.create(feed=self.feed_2, user=self.user)

    def test_success(self):
        body = {}
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)

    def test_feed_not_found(self):
        body = {
            'feed_pk': -1
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

    def test_filter_by_feed(self):
        body = {
            'feed_pk': self.feed_2.pk
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_size'], 0)

    def test_filter_by_read(self):
        body = {
            'is_read': True
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_size'], 1)

    def test_filter_by_followed(self):
        body = {
            'is_feed_followed': True
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_size'], 0)

    def test_filter_by_page(self):
        body = {
            'page': 2
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['posts']), 3)

    def test_filter_by_page_size(self):
        body = {
            'page_size': 5
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.token.token}'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['posts']), 5)
