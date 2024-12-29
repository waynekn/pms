from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password
from apps.organizations import models


class OrganizationModelTest(TestCase):
    """
    Tests for the Organization model.
    """

    def test_organization_creation(self):
        """
        Test for creating an organization.

        This test ensures that:
        - The organization is created with the correct name.
        - The organization's name slug matches the provided slug.
        - The password is hashed correctly.
        """
        organization_name = 'Test org'
        organization_name_slug = slugify(organization_name)
        organization_password = make_password('securepassword123')

        organization = models.Organization.objects.create(
            organization_name=organization_name, organization_name_slug=organization_name_slug,
            organization_password=organization_password)

        self.assertIsInstance(organization, models.Organization)
        self.assertEqual(organization.organization_name, organization_name)
        self.assertEqual(organization.organization_name_slug,
                         organization_name_slug)
        self.assertEqual(organization.organization_password,
                         organization_password)

    def test_changing_organization_password(self):
        """
        Tests that an organization's password is updated correctly.

        This test ensures that:
         - The new password is updated correctly as the organization's password.
        """
        organization_name = 'Test org'
        organization_name_slug = slugify(organization_name)
        organization_password = make_password('securepassword123')

        organization = models.Organization.objects.create(
            organization_name=organization_name, organization_name_slug=organization_name_slug,
            organization_password=organization_password)

        new_password = 'newsecurepassword123'

        organization.set_organization_password(new_password)

        organization.refresh_from_db()

        self.assertTrue(check_password(
            new_password, organization.organization_password))
