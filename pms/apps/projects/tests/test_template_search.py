from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from apps.projects import models
from apps.users.models import User


class TemplateSearchTests(APITestCase):
    """
    Tests for searching for templates.
    """

    def setUp(self):
        """
        Create a user and a template.
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

        self.url = reverse('template_search')

    def test_users_can_search_for_template(self):
        """
        Test that a user can search for templates.
        """
        data = {'name': 't'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
