import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.projects import models
from apps.users.models import User
from apps.organizations.models import Organization


class UserProjectRetrievalListTest(APITestCase):
    """
    Tests for retrieving all projects a user is a member of.
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
        url = reverse('create_project')
        data = {
            'organization': f'{self.organization.organization_id}',
            'project_name': 'test project',
            'description': 'project description',
            'deadline': f'{datetime.date.today() + datetime.timedelta(days=1)}'
        }
        self.project_response = self.client.post(url, data, format='json')

        #########################
        # url
        self.url = reverse('user_project_list')

    def test_user_can_retrieve_projects_they_are_a_member_of(self):
        """
        Tests a user can get all projects that they are a member of
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(self.project_response.data['project_id'],
                         response.data[0]['project_id'])
