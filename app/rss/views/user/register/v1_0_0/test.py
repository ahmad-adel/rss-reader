from accounts.models import User
from django.test import TestCase, Client


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/user/register/'

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

    def test_email_exists(self):
        self.user = User.objects.create(
            email='test@user.com',
        )

        body = {
            'email': 'test@user.com',
            'password': 'password',
        }
        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        data = response.json()
        self.assertEqual(data['message'], "Email already registered.")
