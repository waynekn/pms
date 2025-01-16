from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.organizations.models import OrganizationMember
from apps.users.models import User


class TestOrgAdminCreation(APITestCase):

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

        self.user2 = User.objects.create_user(
            username='testuser2', email='testmail2@test.com', password='securepassword123'
        )

        # manually create an organization memeber who by default wont be an admin
        OrganizationMember.objects.create(organization_id=self.org_res.data['organization_id'],
                                          user=self.user2)

        self.data = {
            'members': [self.user2.username]
        }

        self.url = reverse('create_admins', kwargs={
                           'organization_id': self.org_res.data['organization_id']})

    def test_org_admin_can_assign_admin_privilledges(self):
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_org_admin_can_assign_admin_privilledges(self):
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)

        response = client2.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_payload_fails(self):
        data = {
            **self.data,
            'members': []
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
