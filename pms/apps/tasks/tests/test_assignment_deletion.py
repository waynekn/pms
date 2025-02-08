import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.projects.models import ProjectPhase
from apps.tasks.models import TaskAssignment
from apps.users.models import User


class TaskAssignMentDeletionTests(APITestCase):
    def setUp(self):
        ############################
        # create users
        self.project_manager = User.objects.create_user(
            username='manager', email='managermail@test.com', password='securepassword123'
        )
        self.manager_client = APIClient()
        self.manager_client.force_authenticate(user=self.project_manager)
        self.project_member = User.objects.create_user(
            username='member', email='membermail@test.com', password='securepassword123'
        )
        self.member_client = APIClient()
        self.member_client.force_authenticate(user=self.project_member)

       ####################################
        # create an organization.
        organization_url = reverse('create_organization')
        organization_data = {'organization_name': 'Test org',
                             'organization_password': 'securepassword123',
                             'password2': 'securepassword123'
                             }
        self.organization = self.manager_client.post(
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
        self.project = self.manager_client.post(
            project_url, project_data, format='json')

        ################################
        # create a custom phase.
        phase_url = reverse('create_project_phase', kwargs={
            'project_id': f'{self.project.data['project_id']}'})
        phase_data = {'name': 'custom_phase'}
        self.custom_phase = self.manager_client.post(
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
        task_response = self.manager_client.post(
            task_url, task_data, format='json')
        self.task = task_response.data

        ##############################
        # assign the user a task.
        assignment_url = reverse('assign_task', kwargs={
            'task_id': self.task['task_id']})
        data = {
            'assignees': [self.project_member.username]
        }
        self.manager_client.post(assignment_url, data, format='json')

        # create test data
        self.test_data = {
            'assignee': self.project_member.username
        }

        self.url = reverse('delete_task_assignment', kwargs={
            'task_id': self.task['task_id']})

    def test_task_assignment_deletion_succeeds_for_project_manager(self):
        """
        Test that a project manager can successfully delete a task assignment.
        """
        response = self.manager_client.delete(self.url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username=self.project_member.username)
        self.assertRaises(
            TaskAssignment.DoesNotExist,
            lambda: TaskAssignment.objects.get(
                task=self.task['task_id'], user=user)
        )

    def test_deletion_requires_project_manager_role(self):
        """
        Test that a non-project manager cannot delete a task assignment.
        """
        response = self.member_client.delete(self.url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deletion_requires_existent_assignee(self):
        """
        Test that task assignment cannot be deleted if the assignee does not exist.
        """
        # Post a user who does not exist
        data = {
            **self.test_data,
            'assignee': 'nonexistentuser'
        }
        response = self.manager_client.delete(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deletion_requires_existent_task(self):
        """
        Test that task assignment cannot be deleted if the task does not exist.
        """
        # Pass non-existent task id
        url = reverse('delete_task_assignment', kwargs={
            'task_id': 'wrong_id'})

        response = self.manager_client.delete(url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deletion_requires_existing_task_assignment(self):
        """
        Test that task assignment cannot be deleted if the user is not assigned to the task.
        """
        # Create a user who has not been assigned the task
        user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        data = {
            **self.test_data,
            'assignee': user.username
        }

        response = self.manager_client.delete(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
