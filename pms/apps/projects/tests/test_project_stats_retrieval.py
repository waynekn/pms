import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.projects import models
from apps.users.models import User
from apps.organizations.models import Organization


class ProjectStatisticsRetreivalTests(APITestCase):
    """
    Tests for retrieving a projects statistics.
    """

    def setUp(self):
        """
        Create a user, an organization and a project.
        """

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

        #########################
        # url
        self.url = reverse('project_stats')

    def test_project_stats_retrieval(self):
        """
        Test that users can retreive project statistcs.
        """

        response = self.client.get(
            f'{self.url}?pk={self.project.pk}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tasks', response.data)
        self.assertIn('members', response.data)
        self.assertIn('description', response.data)
        self.assertIn('tasks_in_progress', response.data)
        self.assertIn('tasks_on_hold', response.data)
        self.assertIn('tasks_completed', response.data)
        self.assertIn('percentage_completion', response.data)

    def test_query_with_missing_pk_fail(self):
        """
        Test that a request with missing primary key fails.
        """

        response = self.client.get(f'{self.url}?pk=''')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stats_retrieval_for_non_existent_project(self):
        """
        Test that a 404 error is returned when no project could be found.
        """

        # wrong pk
        response = self.client.get(f'{self.url}?pk=12345/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
