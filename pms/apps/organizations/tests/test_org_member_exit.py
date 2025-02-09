from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User
from apps.organizations import models


class TestOrganizationMemberExit(APITestCase):
    """
    Tests for exiting an organization.
    """

    def setUp(self):
        # create users
        self.admin = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)

        self.member = User.objects.create_user(
            username='member', email='membermail@test.com', password='securepassword123'
        )
        self.member_client = APIClient()
        self.member_client.force_authenticate(user=self.member)

        # create an organization.
        organization = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }
        url = reverse('create_organization')
        org_res = self.admin_client.post(url, data=organization)
        self.org_id = org_res.data['organization_id']

        # create an organization member.

        models.OrganizationMember.objects.create(
            organization_id=self.org_id, user=self.member)

        self.url = reverse('exit_org', kwargs={
                           'organization_id': self.org_id})

    def test_member_can_exit_organization(self):
        response = self.member_client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(
            models.OrganizationMember.DoesNotExist,
            lambda: models.OrganizationMember.objects.get(
                organization=self.org_id, user=self.member)
        )

    def test_org_must_have_1_admin(self):
        # try exiting the organization with the admin client,
        # the only administrator of the organization.
        response = self.admin_client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_exit_org_if_there_are_other_admins(self):
        # make the non admin org member an admin.
        membership = models.OrganizationMember.objects.get(
            organization=self.org_id, user=self.member)
        membership.role = models.OrganizationMember.ADMIN
        membership.save()

        response = self.admin_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(
            models.OrganizationMember.DoesNotExist,
            lambda: models.OrganizationMember.objects.get(
                organization=self.org_id, user=self.admin)
        )
