from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User


class OrganizationAuthenticationTests(APITestCase):
    """
    Tests the authentication feature of organization to become an organization
    member.
    """

    def setUp(self):
        """
        Set up an organization, an organization member(creator of the organization)
        and a user who is not a member of the organization.
        """
        self.user = User.objects.create_user(
            username='orgmember', email='member@test.com', password='securepassword123'
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
        # create an organization.
        self.client.post(url, data, format='json')
        self.url = reverse('organization_auth')

    def test_non_members_can_authenticate_to_become_organization_members(self):
        """
        Test that a user who is not a member of an organization can authenticate
        to join an organization.
        """

        non_member = User.objects.create_user(
            username='nonorgmember', email='nonmember@test.com', password='securepassword123'
        )

        client = APIClient()
        client.force_authenticate(user=non_member)

        credentials = {'password': 'securepassword123',
                       'organizationName': 'Test org'}

        response = client.post(self.url, credentials, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_auth_credentials_fail(self):
        """
        Tests that requests with wrong credentials and payload fails.

        This test ensures that:
         - A request with a wrong passwrod fails.
         - A request with wrong payload fails.
         - A request with wrong organization name fails.
        """
        non_member = User.objects.create_user(
            username='nonorgmember', email='nonmember@test.com', password='securepassword123'
        )

        wrong_password = {
            'password': 'wrongpassword123',
            'organizationName': 'Test org'
        }

        client = APIClient()
        client.force_authenticate(user=non_member)
        response = client.post(self.url, wrong_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        wrong_payload = {
            'password': 'securepassword123',
            'organization': 'Test org'
        }

        response = client.post(self.url, wrong_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        wrong_org_name = {
            'password': 'securepassword123',
            'organizationName': 'wrong org'
        }

        response = client.post(self.url, wrong_org_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
