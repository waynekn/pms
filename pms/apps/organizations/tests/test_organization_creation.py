from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User


class TestOrganizationCreation(APITestCase):
    """
    Tests for creating an organization.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.organization = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }
        self.url = reverse('create_organization')

    def test_organization_creation_from_view(self):
        """
        Tests that a valid organization creation request creates a new organization.

        This test ensures that:
         - The response status code is 201 created.
         - The organization_name is in the response.
        """

        response = self.client.post(self.url, self.organization, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('organization_name', response.data)

    def test_organization_creation_with_password_mismatch(self):
        """
        Test that the organization creation fails if passwords don't match.
        It ensures that the password mismatch is added as a non_field_error.
        """

        organization = {
            ** self.organization,
            'password2': 'differentpassword123',
        }
        response = self.client.post(self.url, organization, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)

    def test_organization_creation_with_missing_name(self):
        """
        Test that the organization creation fails if no organization name is provided.
        """

        organization = self.organization
        del organization['organization_name']
        response = self.client.post(self.url, organization, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('organization_name', response.data)

    def test_organization_creation_with_duplicate_name(self):
        """
        Test that organization creation fails if an organization with 
        the same name already exists.
        """

        self.client.post(self.url, self.organization, format='json')

        response = self.client.post(self.url, self.organization, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('organization_name', response.data)
