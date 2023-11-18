from accounts.models import User
from django.test import TestCase, Client


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/user/login/'
        self.user = User.objects.create(
            email='test@user.com',
        )
        self.user.set_password('password')
        self.user.save()

    def test_success(self):
        body = {
            'email': 'test@user.com',
            'password': 'password',
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

    def test_incorrect_email(self):
        body = {
            'email': 'wrong',
            'password': 'password',
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['message'], "Authentication Failed. Please check your credentials.")

    def test_incorrect_password(self):
        body = {
            'email': 'test@user.com',
            'password': 'wrong',
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['message'], "Authentication Failed. Please check your credentials.")
