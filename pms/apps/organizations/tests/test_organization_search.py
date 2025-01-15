from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User
from rest_framework.utils.serializer_helpers import ReturnList


class OrganizationSearchTest(APITestCase):
    """
    Tests for searching for organizations.
    """

    def setUp(self):
        """
        Set up an organization and user
        """
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('create_organization')

        data = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }

        self.client.post(url, data, format='json')
        self.url = reverse('organization_search')

    def test_users_can_search_for_organizations(self):
        """
        Tests that a user can search for organizations.

        This test ensures that:
         - The response status code is HTTP 200 OK.
        """

        url = self.url + f'?name={'T'}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, ReturnList)
