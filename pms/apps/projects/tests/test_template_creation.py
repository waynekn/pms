import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITransactionTestCase
from apps.projects import models
from apps.users.models import User


class TestTemplateCreation(APITransactionTestCase):
    """
    Tests for creating a template.
    """

    def setUp(self):
        """
        Create a user and industry.
        """
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        industry = models.Industry.objects.create(
            industry_name="Test industry"
        )

        self.data = {
            'industry': f'{industry.pk}',
            'template_name': 'test template',
            'template_phases': ['do x', 'do y', 'do z']
        }

    def test_users_can_create_templates(self):
        """
        Test that users can create a template.
        """
        url = reverse('create_template')

        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_template_name_must_be_less_than_50_chars(self):
        """
        Test that template name must be less than 50 characters.

        This test ensures that:
            - A request to create a template with a name that exceedes max length fails.
            - The response has 'template_name' to provide feedback that the
              name is the problem.
        """
        url = reverse('create_template')

        # ensure template name length is greater than 50
        data = {
            ** self.data,
            'template_name': 'a' * 60
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('template_name', response.data)

    def test_no_duplicate_template_names_in_industry(self):
        """
        Test that templates can't have duplicate names in an industry.

        This test ensures that:
            - A request to create a template with an existing name fails.
            - The response has 'template_name' to provide feedback that the
              name is the problem.
        """
        url = reverse('create_template')

        # create template
        self.client.post(url, self.data, format='json')

        # ensure template workflow is different.
        data = {
            ** self.data,
            'template_phases': ['xyz']
        }

        # attempt to create another template with the same name.
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('template_name', response.data)

    def test_no_different_templates_with_same_workflow_in_industry(self):
        """
        Test that no different templates in the industry can have the same workflow.

        This test ensures that:
            - A request to create a template with an existing name fails.
            - The response has 'template_phases' to provide feedback that the workflow
              is the problem.
        """
        url = reverse('create_template')

        # create template
        self.client.post(url, self.data, format='json')

        # ensure template name is different
        data = {
            **self.data,
            'template_name': "duplicate workflow template",
        }

        # attempt to create a template with same worklow.
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('template_phases', response.data)

    def test_valid_industry_in_creating_template(self):
        """
        Test that a template must be created with an existing industry.

        This test ensures that:
            - A request to create a template with an industry that doesn't exist fails.
            - The response has 'industry' to provide feedback that the
              industry is the problem.
        """

        url = reverse('create_template')

        # put an invalid industry pk.
        data = {
            **self.data,
            'industry': f'{uuid.uuid4()}'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn('industry', response.data)
