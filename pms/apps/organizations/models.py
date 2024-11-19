import uuid
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password, check_password
from apps.users.models import User


class Organization(models.Model):
    """
    Each project must belong to an organization.
    """
    organization_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='Organization ID')
    organization_name = models.CharField(
        max_length=50, unique=True, verbose_name='Organization name')
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organizations', verbose_name='Admin')
    organization_password = models.CharField(
        max_length=255, verbose_name='Organization password')

    def set_organization_password(self, password: str) -> None:
        """
        Validates a plain text password. If the password passes validation, it's hashed 
        and set as the organization's password; otherwise, raises a ValidationError.
        """
        validate_password(
            password)  # Raises ValidationError if validation fails

        self.organization_password = make_password(
            password)  # Hash the password

    def check_organization_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the stored organization's hashed password.
        """
        return check_password(password, self.organization_password)

    def __str__(self) -> str:
        return self.organization_name


class OrganizationMembers(models.Model):
    """
    Users who successfully authenticate themselves via the organization's password are added as its members.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='members', verbose_name='Organization')
    user = models.ForeignKey(
        # Ensure a user can only be a member of an organization once
        User, on_delete=models.CASCADE, verbose_name='Member user')

    class Meta:
        unique_together = ('organization', 'user')

    def __str__(self) -> str:
        return f'{self.organization.organization_id} | {self.user.username}'
