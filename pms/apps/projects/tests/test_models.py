import uuid
from django.test import TestCase
from apps.projects import models


# `Industry` model tests.
class IndustryModelTest(TestCase):
    """
    Unit test for the Industry model.

    This test suite verifies that industries are being created correctly in the database. 
    It checks that an instance of the Industry model is created with the correct attributes 
    and that the industry_id is properly generated as a UUID.

    Test cases:
        - test_industry_creation: Verifies that an Industry object is created with a valid 
          industry_name and a UUID for industry_id.
    """

    def test_industry_creation(self):
        industry = models.Industry.objects.create(
            industry_name="Technology"
        )
        self.assertIsInstance(industry, models.Industry)
        self.assertEqual(industry.industry_name, "Technology")
        self.assertTrue(isinstance(industry.industry_id, uuid.UUID))


# `Template` model tests.


class TemplateModelTest(TestCase):
    """
    Unit test for `Template` model.
    """

    def setUp(self):
        self.industry = models.Industry.objects.create(
            industry_name="Technology"
        )

    def test_template_creation(self):
        """
        Verifies the correct creation of a Template object in the database.

        This test ensures that:
        - The Template instance is created with the correct name.
        - The template_id is generated as a valid UUID.
        - The industry foreign key correctly references an existing Industry.
        """
        self.template = models.Template.objects.create(
            industry=self.industry, template_name="Test template"
        )
        self.assertIsInstance(self.template, models.Template)
        self.assertEqual(self.template.template_name, "Test template")
        self.assertTrue(isinstance(self.template.template_id, uuid.UUID))

    def test_template_industry_updated_to_default_on_deletion(self):
        """
        Test that when an Industry is deleted, the Template is updated
        to use the default industry.
        """
        template = models.Template.objects.create(
            industry=self.industry, template_name="Test template for deletion"
        )

        test_industry = models.Industry.objects.get(pk=self.industry.pk)
        test_industry.delete()

        # Refresh the template object from the database to reflect any changes
        template.refresh_from_db()

        # Retrieve or create the default industry (which is "Other")
        default_industry = models.Industry.objects.get(industry_name="Other")

        self.assertEqual(template.industry, default_industry)
