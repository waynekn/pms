import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.projects import models
from apps.users.models import User
from apps.organizations.models import Organization


class CustomProjectPhaseCreationTests(APITestCase):
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
        organization_url = reverse('create_organization')
        data = {'organization_name': 'Test org',
                'organization_password': 'securepassword123',
                'password2': 'securepassword123'
                }
        self.organization = self.client.post(
            organization_url, data, format='json')

        ##################################
        # create a project.
        self.data = {
            'organization': f'{self.organization.data['organization_id']}',
            'project_name': 'test project',
            'description': 'project description',
            'deadline': f'{datetime.date.today() + datetime.timedelta(days=1)}'
        }
        project_url = reverse('create_project')
        self.project = self.client.post(project_url, self.data, format='json')

        #########################
        # url
        self.url = reverse('create_project_phase', kwargs={
                           'project_id': f'{self.project.data['project_id']}'})

    def test_custom_project_phase_can_be_created(self):
        data = {'name': 'custom_phase'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_duplicate_custom_phase_name(self):
        """
        Test the name of a phase must be unique in a project.
        """

        data = {'name': 'custom_phase'}
        self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
