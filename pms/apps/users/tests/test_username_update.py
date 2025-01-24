from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.users.models import User


class UpdateUsernameTests(APITestCase):
    def setUp(self):
        ############################
        # create test user
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = reverse('username_update')

    def test_user_can_change_username(self):
        response = self.client.put(self.url, {'username': 'newusername'})
        user = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user['username'], "newusername")

    def test_username_must_be_unique(self):
        response = self.client.put(self.url, {'username': self.user.username})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_must_be_valid(self):
        response = self.client.put(self.url, {'username': "#username"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.url, {'username': "user  name"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payload_must_contain_username_key(self):
        response = self.client.put(self.url, {'wrongkey': self.user.username})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
