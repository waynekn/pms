import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.tasks import models
from apps.organizations.models import Organization
from apps.projects.models import (
    Project, ProjectPhase, CustomPhase, ProjectMember)
from apps.users.models import User


class TaskAssignMentTest(APITestCase):
    def setUp(self):
        ############################
        # create users
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', email='testmail2@test.com', password='securepassword123'
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

        ##################################
        # add both users as project members.
        ProjectMember.objects.create(project=self.project, member=self.user)
        ProjectMember.objects.create(project=self.project, member=self.user2)
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

        ###########################
        # assign `self.user` a task
        models.TaskAssignment.objects.create(
            user=self.user, task=self.task
        )

        self.url = reverse('non_assignees', kwargs={'task_id': self.task.pk})

    def test_retrieval_of_non_task_assignees(self):
        """
        Test retrieval of users who are members of a project
        but have not been assigned a task.
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['username'], self.user2.username)
