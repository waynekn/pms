import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITransactionTestCase
from rest_framework import status

from apps.projects import models
from apps.users.models import User
from apps.organizations.models import Organization


class ProjectMemberAdditionTests(APITransactionTestCase):
    """
    Tests for adding users to a project.
    """

    def setUp(self):
        ####################################
        # create a user.
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        ####################################
        # create an organization.
        organization_name = 'Test org'
        organization_name_slug = 'test-org'
        organization_password = 'securepassword123'

        self.organization = Organization.objects.create(
            organization_name=organization_name, organization_name_slug=organization_name_slug,
            organization_password=organization_password)

        ##################################
        # create a project.
        deadline = datetime.date.today() + datetime.timedelta(days=1)

        self.project = models.Project.objects.create(
            organization=self.organization, project_name="Test project",
            description='Testing project creation', deadline=deadline)

        models.ProjectMember.objects.create(
            project=self.project, member=self.user)

        #########################
        # url
        self.url = reverse('project_members_addition', kwargs={
                           'project_id': f'{self.project.pk}'})

    def test_project_manager_can_add_users_to_a_project(self):
        User.objects.create_user(
            username='nonmember', email='nonmember@test.com', password='securepassword123')

        data = {'members': ['non_member']}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.project.members.count(), 2)

    def test_request_with_invalid_payload_fails(self):
        response = self.client.post(self.url, {'members': []}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
