from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest
from .models import User


class EmailAuthBackend(BaseBackend):
    """
    Allow users to log in with their email
    """

    def authenticate(self, request: HttpRequest, username: str = None, password: str = None, **kwargs: Any) -> AbstractUser | None:
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id) -> AbstractUser | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
