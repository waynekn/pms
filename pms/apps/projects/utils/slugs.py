from django.utils.text import slugify
from ..models import Project


def slugify_project_name(project_name: str) -> str:
    """
    Slugify the project name and ensure it is unique.
    """
    project_name_slug = slugify(project_name)

    counter = 1
    while Project.objects.filter(project_name_slug=project_name_slug).exists():
        project_name_slug = f"{project_name_slug}-{counter}"
        counter += 1

    return project_name_slug
