from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User


class OrganizationViewTests(APITestCase):
    """
    Tests for `organizations` app views.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_organization_creation_from_view_creates_new_organization(self):
        """
        Tests that a valid organization creation request creates a new organization.

        This test ensures that:
         - The response status code is 201 created.
         - The organization_name is in the response.
        """

        url = reverse('create_organization')
        data = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('organization_name', response.data)
