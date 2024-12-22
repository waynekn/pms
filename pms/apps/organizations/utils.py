from django.utils.text import slugify
from .models import Organization


def slugify_organization_name(organization_name: str) -> str:
    """
    Slugify the organization name and ensure it is unique.
    """
    organization_name_slug = slugify(organization_name)

    counter = 1
    while Organization.objects.filter(organization_name_slug=organization_name_slug).exists():
        organization_name_slug = f"{organization_name_slug}-{counter}"
        counter += 1

    return organization_name_slug
