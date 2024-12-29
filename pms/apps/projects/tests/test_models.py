import uuid
import datetime
from django.test import TestCase
from apps.projects import models
from django.utils.text import slugify
from apps.organizations.models import Organization

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
        template = models.Template.objects.create(
            industry=self.industry, template_name="Test template"
        )
        self.assertIsInstance(template, models.Template)
        self.assertEqual(template.template_name, "Test template")
        self.assertTrue(isinstance(template.template_id, uuid.UUID))

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


# `Project` model test.
class ProjectModelTest(TestCase):
    """
    Tests for the `Project` model
    """

    def setUp(self):
        """
        Set up a test Organization and Template instance.
        """
        organization_name = "Test org"
        organization_name_slug = slugify(organization_name)
        self.organization = Organization.objects.create(
            organization_name=organization_name, organization_name_slug=organization_name_slug,
            organization_password="securepassword123")

        ############################
        # set up a Template instance
        ############################

        industry = models.Industry.objects.create(
            industry_name="Test industry.")
        template_name = 'Project creation template'
        self.template_phases = ['do x', 'do y', 'do z']
        self.template = models.Template.objects.create(
            industry=industry, template_name=template_name)
        models.TemplatePhase.objects.bulk_create([
            models.TemplatePhase(template=self.template, phase_name=phase_name)
            for phase_name in self.template_phases
        ])

    def test_project_creation(self):
        """
        Tests the correct creation of a project.

        This test ensures that:
         - The project instance is created with the correct name.
         - The project_id is generated as a valid UUID.
         - The organization foreign key correctly references an existing organization.
         - The description matches the provided description.
         - The deadline is an instance of datetime.date.
         - The status defaults to 'IN_PROGRESS'
        """

        deadline = datetime.date.today() + datetime.timedelta(days=1)
        description = 'Testing project creation'

        project = models.Project.objects.create(
            organization=self.organization, project_name="Test project",
            description='Testing project creation', deadline=deadline)

        self.assertIsInstance(project, models.Project)
        self.assertIs(project.organization, self.organization)
        self.assertIsInstance(project.project_id, uuid.UUID)
        self.assertEqual(project.description, description)
        self.assertIs(project.deadline, deadline)
        self.assertIsInstance(project.deadline, datetime.date)
        self.assertEqual(project.status, "IN_PROGRESS")

    def test_project_creation_from_template(self):
        """
        Test creating a project from a template.

        This test ensures that:
         - The project is using the correct template.
         - The project's workflow matches the template's workflow.
        """
        deadline = datetime.date.today() + datetime.timedelta(days=1)
        description = 'Testing project creation from template'

        project = models.Project.objects.create(
            organization=self.organization, project_name="Test template project", template=self.template,
            description=description, deadline=deadline)

        self.assertIs(project.template, self.template)

        phase_names = [
            phase.phase_name for phase in project.template.phases.all()]
        self.assertListEqual(phase_names, self.template_phases)
