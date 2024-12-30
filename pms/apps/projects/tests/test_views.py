from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from apps.projects import models
from apps.users.models import User


class TestIndustryListRetrieval(APITestCase):
    """
    Tests that a list of all industries in the system can be
    retreived.
    """

    def setUp(self):
        """
        Create an industry and user.
        """
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        models.Industry.objects.create(
            industry_name="Test industry"
        )

    def test_industry_retrieval(self):
        """
        Tests that the API returns a list of industries with a 200 OK status.

        Verifies that:
            - The response status code is 200 OK.
            - The response data is a list.
            - The list contains the created industry.
        """
        url = reverse('industry_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
