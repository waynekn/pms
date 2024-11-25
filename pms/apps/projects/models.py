import uuid
from django.db import models

# Create your models here.


class Industry(models.Model):
    """
    Represents an industry category for organizing project templates.

    The `Industry` model is used to classify templates into specific categories 
    based on industry type. This categorization helps users easily find and 
    apply relevant templates for their projects. Each industry is uniquely identified
    by an `industry_id`, which is a UUID.

    Attributes:
        industry_id (UUIDField): A unique identifier for the industry.
        industry_name (CharField): The name of the industry e.g., 'Construction'.
    """

    industry_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    industry_name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.industry_name


def get_default_industry():
    """
    Retrieves the default industry to be used when a template references a deleted industry.

    Returns:
        UUID: The unique identifier (industry_id) of the default industry, 
            which is the "Other" industry.
    """
    industry = Industry.objects.get_or_create(industry_name="Other")
    return industry.pk


class Template(models.Model):
    """
    Represents a reusable project template that is categorized by industry.

    The `Template` model stores project templates that users can apply to their own 
    projects. Each template is linked to a specific `Industry`, allowing for better 
    organization and searchability.

    Attributes:
        industry_id (ForeignKey): A reference to the `Industry` that the template 
                                   belongs to. If the industry is deleted, it is 
                                   set to the default industry using `get_default_industry`.
        template_id (UUIDField): A unique identifier for the template, automatically 
                                 generated using UUID.
        template_name (CharField): The name of the template, which should be unique 
                                   within the database.
    """
    industry_id = models.ForeignKey(Industry, on_delete=models.SET_DEFAULT,
                                    default=get_default_industry)
    template_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4)
    template_name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.template_name
