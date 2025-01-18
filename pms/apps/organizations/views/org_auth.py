from django.contrib.auth.hashers import check_password

from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.response import Response

from apps.organizations import models


class OrganizationAuthView(generics.CreateAPIView):
    """
    Handles the authorization process for a user to join an organization as an `OrganizationMember`.

    This view expects the following data in the request body:
        - `organizationName`: The name of the organization the user wants to join.
        - `password`: The password associated with the organization.

    Responses:
        - 201 Created: If the user is successfully added as an `OrganizationMember`.
        - 400 Bad Request: If the credentials are invalid (either the organization doesn't exist, 
          the password is incorrect, or the password is missing).
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        organization_name = request.data.get('organizationName')
        password = request.data.get('password')

        try:
            organization = models.Organization.objects.get(
                organization_name=organization_name)
        except models.Organization.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        password = password.strip() if password else None

        if not password:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, organization.organization_password):
            models.OrganizationMember.objects.create(
                organization=organization, user=self.request.user)
            return Response(status=status.HTTP_201_CREATED)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
