from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class AccountRegistrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # this data is valid to create a user.
        self.data = {
            'username': 'test user',
            'email': 'testmail@gmail.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }

        self.url = reverse('account_registration')

    def test_account_is_successfully_created(self):
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.data['username'])

    def test_username_uniqueness(self):
        self.client.post(self.url, self.data)

        # change email to make sure it wont be the cause of a 400
        data = {
            **self.data,
            'email': 'randommail@gmail.com'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_email_uniqueness(self):
        self.client.post(self.url, self.data)

        # change username to make sure it wont be the cause of a 400
        data = {
            **self.data,
            'username': 'another name'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_passwords_must_match(self):
        data = {
            **self.data,
            'password2': 'securepassword345'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_password_strength_requirement(self):
        data = {
            **self.data,
            'password1': '123',
            'password2': '123',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', response.data)

    def test_missing_required_fields(self):
        # Missing username
        data = {
            'email': 'testmail@gmail.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

        # Missing password fields
        data = {
            'username': 'testuser',
            'email': 'testmail@gmail.com',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', response.data)

    def test_invalid_email_format(self):
        data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
