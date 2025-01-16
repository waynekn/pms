from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.organizations.models import OrganizationMember
from apps.users.models import User


class TestRetrievalOfNonOrgAdmins(APITestCase):
    """
    Tests retrieval of organization members who are not admins.
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
        org_create_url = reverse('create_organization')

        self.org_res = self.client.post(
            org_create_url, self.organization, format='json')

        user2 = User.objects.create_user(
            username='testuser2', email='testmail2@test.com', password='securepassword123'
        )

        # manually create an organization memeber who by default wont be an admin
        OrganizationMember.objects.create(organization_id=self.org_res.data['organization_id'],
                                          user=user2)

        self.url = reverse('non_org_admins', kwargs={
                           'organization_id': self.org_res.data['organization_id']})

    def test_organization_admin_retrieval(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
