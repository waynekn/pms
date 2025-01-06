from django.utils.text import slugify
from .models import User


def slugify_username(username: str) -> str:
    """
    Slugify the username and ensure it is unique.
    """
    username_slug = slugify(username)

    counter = 1
    while User.objects.filter(username_slug=username_slug).exists():
        username_slug = f"{username_slug}-{counter}"
        counter += 1

    return username_slug
