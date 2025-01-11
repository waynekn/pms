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
        # create task
        deadline = (datetime.date.today() +
                    datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        self.task = models.Task.objects.create(
            project=self.project, project_phase=self.project_phase, task_name='test task',
            description='task description', deadline=deadline,
        )

        self.url = reverse('assign_task', kwargs={'task_id': self.task.pk})

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
            task_id=self.task.pk)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(task_assignments), 2)

    def test_no_duplicate_task_assignment(self):
        data = {'assignees': [self.user.username]}

        self.client.post(self.url, data, format='json')
        self.client.post(self.url, data, format='json')

        task_assignments = models.TaskAssignment.objects.filter(
            task_id=self.task.pk)

        self.assertEqual(len(task_assignments), 1)

    def test_task_assignment_with_nonexistent_task_id_returns_400(self):
        url = reverse("assign_task", kwargs={'task_id': '123'})

        data = {'assignees': [self.user.username]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
