from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils.serializer_helpers import ReturnList
from apps.users.models import User


class TestUserOrganizationsRetrieval(APITestCase):
    """
    Tests for retreiving a users organizations.
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

        self.organization = self.client.post(url, data, format='json')

    def test_retrieval_of_user_organizations_list(self):
        """
        Test that the organizations which a user is a member of are retreived.
        """

        url = reverse('user_organizations')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(type(response.data) == ReturnList)
        self.assertEqual(
            response.data[0]['organization_id'], self.organization.data['organization_id'])
