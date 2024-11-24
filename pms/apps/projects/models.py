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
