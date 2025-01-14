import datetime
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APIClient, APITransactionTestCase
from apps.projects import models
from apps.users.models import User
from apps.organizations.models import Organization


class ProjectCreationTests(APITransactionTestCase):
    """
    Tests for creating a project.
    """

    def setUp(self):
        """
        Create a user, an organization and a template.
        """
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        #######################################
        # create an industry
        industry = models.Industry.objects.create(
            industry_name="Test industry"
        )

        #######################################
        # create a template
        self.template = models.Template.objects.create(
            industry=industry, template_name="test template")

        ####################################
        # create an organization.
        organization_url = reverse('create_organization')
        data = {'organization_name': 'Test org',
                'organization_password': 'securepassword123',
                'password2': 'securepassword123'
                }
        self.organization = self.client.post(
            organization_url, data, format='json')

        self.url = reverse('create_project')

        ##################################
        # create test data.
        # this data is valid to create a project without a template.
        self.data = {
            'organization': f'{self.organization.data['organization_id']}',
            'project_name': 'test project',
            'description': 'project description',
            'deadline': f'{datetime.date.today() + datetime.timedelta(days=1)}'
        }

    def test_project_creation_without_template(self):
        """
        Test that a project can be created without a template.
        """

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('organization', response.data)
        self.assertIn('project_name', response.data)
        self.assertIn('description', response.data)
        self.assertIn('deadline', response.data)

    def test_project_creation_from_template(self):
        """
        Test that a project can be created from a template
        """

        # add a template
        data = {
            ** self.data,
            'template': f'{self.template.template_id}',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('organization', response.data)
        self.assertIn('template', response.data)
        self.assertEqual(response.data['template'], self.template.pk)
        self.assertIn('project_name', response.data)
        self.assertIn('description', response.data)
        self.assertIn('deadline', response.data)

    def test_user_is_added_as_project_member(self):
        """
        Test that a user has been added as a project member after creating
        a project.
        """
        response = self.client.post(self.url, self.data, format='json')

        pk = response.data['project_id']

        created_project = models.Project.objects.get(pk=pk)

        members = created_project.members.all()

        member_users = [member.member for member in members]

        self.assertIn(self.user, member_users)

    def test_no_duplicate_project_names_in_an_organization(self):
        """
        Test that a project's name must be unique within the organization.

        This test ensures that:
            - A request to create a project with a duplicate name fails.
            - The response has 'project_name' to provide feedback that the
              project name is the problem
        """
        # create a project
        self.client.post(self.url, self.data, format='json')

        # attempt to another project with the same name
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('project_name', response.data)

    def test_deadline_minimum_must_be_in_the_future(self):
        """
        Test that a project's deadline must be in the future.

        This test ensures that:
            - A request to create a project with a deadline in the past fails.
            - The response has 'deadline' to provide feedback that the
              deadline is the problem
        """

        # set the deadline to yesterday.
        data = {
            ** self.data,
            'deadline': f'{datetime.date.today() + datetime.timedelta(days=-1)}'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('deadline', response.data)

    def test_project_name_length_within_bounds(self):
        """
        Test that a project's name must be between 5 and 50 characters long.

        This test ensures that:
            - A request to create a project with a project name length
              out of bounds fails.
            - The response has 'projet_name' to provide feedback that the
              projet name is the problem
        """

        # set a short project name.
        data = {
            **self.data,
            'project_name': 't'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('project_name', response.data)

        # set a long project name
        data['project_name'] = 't' * 60
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('project_name', response.data)

    def test_description_must_be_500_or_less_chars(self):
        """
        Test that a description must be 500 or less characters.

        This test ensures that:
            - A request to create a project with a description that is too long fails.
            - The response has 'deadline' to provide feedback that the
              deadline is the problem
        """
        # set a long description.
        data = {
            **self.data,
            'description': 'd' * 501
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('description', response.data)
