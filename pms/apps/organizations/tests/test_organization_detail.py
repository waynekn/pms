from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User


class TestOrganizationDetailRetreival(APITestCase):
    """
    Tests for retreiving organization detail.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('create_organization')

        self.organization = {
            'organization_name': 'Test org2',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }

        self.organization = self.client.post(
            url, self.organization, format='json')

        self.url = reverse('organization_detail', kwargs={
                           'organization_name_slug': self.organization.data['organization_name_slug']})

    def test_member_can_access_organization_detail(self):
        """
        Tests that an authenticated user who is a member of an organization 
        can successfully view the organization's details.

        This test ensures the following:
        - The response status code is HTTP 200 OK.
        - The response data is a dictionary.
        - The response dictionary contains a 'projects' key.
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('projects', response.data)
        self.assertIn('role', response.data)

    def test_non_members_cant_access_organization_detail(self):
        """
        Tests that users who are not members of an organization cannot view the
        organization's detail
        """
        user = User.objects.create_user(
            username='nonmember', email='nonmembermail@test.com', password='securepassword123'
        )
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
