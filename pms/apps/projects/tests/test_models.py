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
