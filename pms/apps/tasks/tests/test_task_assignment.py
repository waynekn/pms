import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.tasks import models
from apps.organizations.models import Organization
from apps.projects.models import (Project, ProjectPhase, CustomPhase)
from apps.users.models import User


class TaskAssignMentTest(APITestCase):
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

        task_response = self.client.post(task_url, task_data, format='json')

        self.task = task_response.data

        self.url = reverse('assign_task', kwargs={
                           'task_id': self.task['task_id']})

    def test_tasks_assignment(self):
        user1 = User.objects.create_user(
            username='testuser2', email='testmail2@test.com', password='securepassword123'
        )

        user2 = User.objects.create_user(
            username='testuser3', email='testmail3@test.com', password='securepassword123'
        )

        usernames = [user1.username, user2.username]

        data = {
            'assignees': usernames
        }

        response = self.client.post(self.url, data, format='json')

        task_assignments = models.TaskAssignment.objects.filter(
            task_id=self.task['task_id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(task_assignments), 2)

    def test_no_duplicate_task_assignment(self):
        data = {'assignees': [self.user.username]}

        self.client.post(self.url, data, format='json')
        self.client.post(self.url, data, format='json')

        task_assignments = models.TaskAssignment.objects.filter(
            task_id=self.task['task_id'])

        self.assertEqual(len(task_assignments), 1)

    def test_task_assignment_with_nonexistent_task_id_returns_404(self):
        url = reverse("assign_task", kwargs={'task_id': '123'})

        data = {'assignees': [self.user.username]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_project_manager_can_assign_task(self):
        user = User.objects.create_user(
            username='testuser2', email='testmail2@test.com', password='securepassword123'
        )
        client = APIClient()
        client.force_authenticate(user=user)

        data = {'assignees': [user.username]}
        response = client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
