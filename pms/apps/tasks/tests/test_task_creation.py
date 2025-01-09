import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.organizations.models import Organization
from apps.projects.models import (Project, ProjectPhase, CustomPhase)
from apps.users.models import User


class TaskCreationTests(APITestCase):
    def setUp(self):
        ############################
        # create a user
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

        ###################################
        # create a project.
        deadline = datetime.date.today() + datetime.timedelta(days=1)

        self.project = Project.objects.create(
            organization=self.organization, project_name="Test project",
            description='Testing project creation', deadline=deadline)

        ################################
        # create a custom project phase phase.
        self.custom_phase = CustomPhase.objects.create(
            project=self.project, phase_name='test phase')

        #################################
        # create a project phase.
        self.project_phase = ProjectPhase.objects.create(
            project=self.project, custom_phase=self.custom_phase)

        ############################
        # create data
        deadline = (datetime.date.today() +
                    datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        self.data = {
            'project_phase': f'{self.project_phase.pk}',
            'task_name': "test task",
            'deadline': deadline,
            'description': "task description",
        }

        self.url = reverse('create_task')

    def test_task_creation(self):
        """
        Test that task is created successfully.
        """

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_name_must_be_unique(self):
        self.client.post(self.url, self.data, format='json')

        # try creating a task with the same name.
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_name_length_within_bounds(self):
        # short name
        data = {
            **self.data,
            'task_name': 'a'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # long name
        data = {
            **self.data,
            'task_name': 'a' * 31
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deadline_must_be_in_future(self):
        deadline = deadline = (datetime.date.today() +
                               datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
        data = {
            **self.data,
            'deadline': deadline,
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_description_length_within_bounds(self):
        data = {
            **self.data,
            'description': 'a' * 501,
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
