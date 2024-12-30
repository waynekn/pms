from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


class TestOrganizationCreation(APITestCase):
    """
    Tests for creating an organization.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.organization = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }

    def test_organization_creation_from_view_creates_new_organization(self):
        """
        Tests that a valid organization creation request creates a new organization.

        This test ensures that:
         - The response status code is 201 created.
         - The organization_name is in the response.
        """

        url = reverse('create_organization')
        response = self.client.post(url, self.organization, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('organization_name', response.data)

    def test_organization_creation_password_mismatch(self):
        """
        Test that the organization creation fails if passwords don't match.
        It ensures that the password mismatch is added as a non_field_error.
        """
        url = reverse('create_organization')
        organization = {
            ** self.organization,
            'password2': 'differentpassword123',
        }
        response = self.client.post(url, organization, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)

    def test_create_organization_missing_name(self):
        """
        Test that the organization creation fails if no organization name is provided.
        """
        url = reverse('create_organization')
        organization = self.organization
        del organization['organization_name']
        response = self.client.post(url, organization, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('organization_name', response.data)

    def test_create_organization_duplicate_name(self):
        """
        Test that organization creation fails if an organization with 
        the same name already exists.
        """
        url = reverse('create_organization')

        self.client.post(url, self.organization, format='json')

        response = self.client.post(url, self.organization, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('organization_name', response.data)


class TestUserOrganizationsRetrieval(APITestCase):
    """
    Tests for retreiving a users organizations.
    """

    def setUp(self):
        """
        Set up an organization and user
        """
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('create_organization')

        data = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }

        self.client.post(url, data, format='json')

    def test_retrieve_user_organizations_list(self):
        """
        Test that the organizations which a user is a member of are retreived correctly.
        """

        url = reverse('user_organizations')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(type(response.data) == ReturnList)


class TestOrganizationDetailRetreival(APITestCase):
    """
    Tests for retreiving organization detail.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('create_organization')

        self.organization = {
            'organization_name': 'Test org2',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }

        self.client.post(
            url, self.organization, format='json')

    def test_member_can_access_organization_detail(self):
        """
        Tests that an authenticated user who is a member of an organization 
        can successfully view the organization's details.

        This test ensures the following:
        - The response status code is HTTP 200 OK.
        - The response data is a dictionary.
        - The response dictionary contains a 'projects' key.
        """
        url = reverse('organization_detail')
        query = {
            'organizationNameSlug': slugify(self.organization['organization_name'])
        }
        response = self.client.post(url, query, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, ReturnDict)
        self.assertIn('projects', response.data)

    def test_non_members_cant_access_organization_detail(self):
        """
        Tests that users who are not members of an organization cannot view the
        organization's detail
        """
        user = User.objects.create_user(
            username='nonmember', email='nonmembermail@test.com', password='securepassword123'
        )
        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse('organization_detail')
        query = {
            'organizationNameSlug': slugify(self.organization['organization_name'])
        }
        response = client.post(url, query, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_payload_returns_400(self):
        """
        Test that a bad requ in a 400 bad request to get organization detail results in a 400
        bad request error.
        """
        url = reverse('organization_detail')
        query = {
            'wrong_key': slugify(self.organization['organization_name'])
        }
        response = self.client.post(url, query, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrganizationSearchTest(APITestCase):
    """
    Tests for searching for organizations.
    """

    def setUp(self):
        """
        Set up an organization and user
        """
        self.user = User.objects.create_user(
            username='testuser', email='testmail@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('create_organization')

        data = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }

        self.client.post(url, data, format='json')

    def test_users_can_search_for_organizations(self):
        """
        Tests that a user can search for organizations.

        This test ensures that:
         - The response status code is HTTP 200 OK.
         - The response data is a dictionary.
        """
        url = reverse('organization_search')
        query = {
            'organization_name_query': "T"
        }

        response = self.client.post(url, query, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, ReturnList)

    def test_invalid_request_to_search_organizations(self):
        """
        Test that a bad request to search for organizations results in a 400
        bad request error.
        """
        url = reverse('organization_search')
        query = {
            'name': "T"
        }

        response = self.client.post(url, query, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrganizationAuthenticationTests(APITestCase):
    """
    Tests the authentication feature of organization to become an organization
    member.
    """

    def setUp(self):
        """
        Set up an organization, an organization member(creator of the organization)
        and a user who is not a member of the organization.
        """
        self.user = User.objects.create_user(
            username='orgmember', email='member@test.com', password='securepassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('create_organization')

        data = {
            'organization_name': 'Test org',
            'description': 'organization description',
            'organization_password': 'securepassword123',
            'password2': 'securepassword123',
        }
        # create an organization.
        self.client.post(url, data, format='json')

    def test_non_members_can_authenticate_to_become_organization_members(self):
        """
        Test that a user who is not a member of an organization can authenticate
        to join an organization.
        """
        url = reverse('organization_auth')

        non_member = User.objects.create_user(
            username='nonorgmember', email='nonmember@test.com', password='securepassword123'
        )

        client = APIClient()
        client.force_authenticate(user=non_member)

        credentials = {'password': 'securepassword123',
                       'organizationName': 'Test org'}

        response = client.post(url, credentials, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_auth_credentials_fail(self):
        """
        Tests that requests with wrong credentials and payload fails.

        This test ensures that:
         - A request with a wrong passwrod fails.
         - A request with wrong payload fails.
         - A request with wrong organization name fails.
        """
        url = reverse('organization_auth')
        non_member = User.objects.create_user(
            username='nonorgmember', email='nonmember@test.com', password='securepassword123'
        )

        wrong_password = {
            'password': 'wrongpassword123',
            'organizationName': 'Test org'
        }

        client = APIClient()
        client.force_authenticate(user=non_member)
        response = client.post(url, wrong_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        wrong_payload = {
            'password': 'securepassword123',
            'organization': 'Test org'
        }

        response = client.post(url, wrong_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        wrong_org_name = {
            'password': 'securepassword123',
            'organizationName': 'wrong org'
        }

        response = client.post(url, wrong_org_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
