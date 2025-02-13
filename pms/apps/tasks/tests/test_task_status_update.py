import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.tasks import models
from apps.projects.models import ProjectPhase
from apps.users.models import User


class UpdateTaskStatusTests(APITestCase):
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

        ###################################
        # create a project phase
        self.project_phase = ProjectPhase.objects.create(
            project_id=self.project.data['project_id'],
            phase_name='custom_phase'
        )

        ############################
        # create task
        deadline = (datetime.date.today() +
                    datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        task_data = {
            'project_phase': f'{self.project_phase.pk}',
            'task_name': "test task",
            'deadline': deadline,
            'description': "task description",
        }
        task_url = reverse('create_task')

        self.task = self.client.post(task_url, task_data, format='json')

        self.url = reverse('update_task_status', kwargs={
                           'task_id': self.task.data['task_id']})

    def test_task_status_is_updated(self):
        data = {
            'status': 'ON_HOLD'
        }
        response = self.client.put(self.url, data, format='json')

        task = models.Task.objects.get(pk=self.task.data['task_id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.status, 'ON_HOLD')

    def test_task_status_update_with_invalid_payload(self):
        data = {
            'status': 'hold'
        }
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_existent_task_status_update(self):
        data = {
            'status': 'ON_HOLD'
        }

        url = reverse('update_task_status', kwargs={
            'task_id': '12345'})

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
