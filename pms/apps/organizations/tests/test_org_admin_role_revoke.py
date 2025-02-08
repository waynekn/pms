from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.organizations.models import OrganizationMember
from apps.users.models import User


class TestOrgAdminRemoval(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.user1_client = APIClient()
        self.user1_client.force_authenticate(user=self.user1)
        self.organization = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }
        org_create_url = reverse('create_organization')

        self.org_res = self.user1_client.post(
            org_create_url, self.organization, format='json')

        self.user2 = User.objects.create_user(
            username='testuser2', email='testmail2@test.com', password='securepassword123'
        )

        # create another admin
        OrganizationMember.objects.create(organization_id=self.org_res.data['organization_id'],
                                          user=self.user2, role=OrganizationMember.ADMIN)

        self.data = {
            'admin': self.user2.username
        }
        self.url = reverse('remove_admin', kwargs={
                           'organization_id': self.org_res.data['organization_id']})

    def test_admin_is_revoked(self):
        response = self.user1_client.put(self.url, self.data)
        admin_member = OrganizationMember.objects.get(
            organization=self.org_res.data['organization_id'], user=self.user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_member.role, OrganizationMember.MEMBER)

    def test_only_admin_can_revoke_admin_role(self):
        # create a org member who is not an admin
        org_member = User.objects.create_user(
            username='testuser3', email='testmail3@test.com', password='securepassword123'
        )
        OrganizationMember.objects.create(organization_id=self.org_res.data['organization_id'],
                                          user=org_member)
        client = APIClient()
        client.force_authenticate(user=org_member)

        response = client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_username_must_be_provided(self):
        response = self.user1_client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_does_not_exist(self):
        data = {
            **self.data,
            'admin': 'nonexistentuser'
        }
        response = self.user1_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_organization_must_have_at_least_1_admin(self):
        # delete the second admin
        self.user1_client.put(self.url, self.data)

        # try deleting the only admin
        data = {
            **self.data,
            'admin': self.user1.username
        }

        response = self.user1_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
