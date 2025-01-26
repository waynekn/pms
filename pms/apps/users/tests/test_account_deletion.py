from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.users.models import User


class AccountDeletionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.url = reverse('account_delete')

    def test_successful_account_deletion(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the user does not exist anymore
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user.pk)
