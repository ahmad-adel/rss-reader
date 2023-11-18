from django.conf import settings
from django.test import TestCase, Client
from django.utils import timezone
from accounts.models import User, Token

import datetime


class RefreshTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/user/refresh/'
        self.user = User.objects.create(
            email='test@user.com',
        )
        self.refresh_token = Token.objects.create(user=self.user, type='refresh')

    def test_success(self):
        body = {
            'refresh_token': self.refresh_token.token
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual('access_token' in data, True)
        self.assertEqual('refresh_token' in data, True)

    def test_wrong_token(self):
        body = {
            'refresh_token': 'wrong'
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['message'], "Refresh token invalid.")

    def test_expired_token(self):
        self.refresh_token.creation_time = timezone.now() - datetime.timedelta(seconds=settings.REFRESH_TOKEN_EXPIRY_SECONDS)
        self.refresh_token.save()
        body = {
            'refresh_token': self.refresh_token.token
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['message'], "Refresh token invalid.")
