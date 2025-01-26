import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.projects.models import (ProjectPhase, CustomPhase)
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
        organization_url = reverse('create_organization')
        organization_data = {'organization_name': 'Test org',
                             'organization_password': 'securepassword123',
                             'password2': 'securepassword123'
                             }
        self.organization = self.client.post(
            organization_url, organization_data, format='json')

        ##################################
        # create a project.
        project_data = {
            'organization': f'{self.organization.data['organization_id']}',
            'project_name': 'test project',
            'description': 'project description',
            'deadline': f'{datetime.date.today() + datetime.timedelta(days=1)}'
        }
        project_url = reverse('create_project')
        self.project = self.client.post(
            project_url, project_data, format='json')

        ################################
        # create a custom phase.
        phase_url = reverse('create_project_phase', kwargs={
            'project_id': f'{self.project.data['project_id']}'})

        phase_data = {'name': 'custom_phase'}
        self.custom_phase = self.client.post(
            phase_url, phase_data, format='json')

        ###################################
        # create a project phase
        self.project_phase = ProjectPhase.objects.create(
            project_id=self.project.data['project_id'],
            custom_phase_id=self.custom_phase.data['phase_id']
        )

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
            'task_name': 'a' * 101
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

    def test_only_project_member_can_create_task(self):
        user = User.objects.create_user(
            username='testuser2', email='testmail2@test.com', password='securepassword123'
        )
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
