import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import username_validator

# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only, '
            'with a single space allowed between words.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='email address', blank=False)
    # make field nullable to avoid migration errors
    username_slug = models.SlugField(max_length=200, unique=True, null=True)
    profile_picture = models.CharField(
        max_length=255, help_text='Name of the profile picture in S3 bucket', default='DEFAULTPROFILEPICTURE')

    def __str__(self) -> str:
        return self.username
