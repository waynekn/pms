import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='email address', blank=False)
    # make field nullable to avoid migration errors
    username_slug = models.SlugField(max_length=200, unique=True, null=True)

    def __str__(self) -> str:
        return self.username
