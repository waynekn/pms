import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.tasks import models
from apps.projects.models import ProjectPhase
from apps.users.models import User


class TaskDetailTest(APITestCase):
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

        self.url = reverse('task_detail', kwargs={
                           'task_id': self.task.data['task_id']})

    def test_task_detail_retrieval(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_id'], self.task.data['task_id'])
        self.assertIsInstance(response.data['assignees'], list)

    def test_task_retrieval_with_nonexistent_task_id_returns_404(self):
        url = reverse('task_detail', kwargs={'task_id': '123'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
