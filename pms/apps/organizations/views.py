from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from pms.utils import camel_case_to_snake_case
from apps.projects.serializers import ProjectRetrievalSerializer
from .models import Organization, OrganizationMember
from . import serializers

# Create your views here.


class UserOrganizationListView(APIView):
    """
    Displays a list of organizations that the currently authenticated user
    is a member of.
    """
    model = Organization

    def get(self, request: Request) -> Response:
        # Get all OrganizationMember entries where the user is a member
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user)

        # Get the related Organization objects for those memberships
        organizations = Organization.objects.filter(
            organization_id__in=user_organizations.values('organization_id')
        )

        serializer = serializers.OrganizationRetrievalSerializer(
            organizations, many=True)
        return Response(serializer.data)


class OrganizationCreateView(generics.CreateAPIView):
    """
    Creates an organization, saves it to the database and adds the
    user who creates the organization to its members.
    """
    model = Organization
    serializer_class = serializers.OrganizationCreationSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        transformed_data = camel_case_to_snake_case(request.data)
        serializer = self.get_serializer(
            data=transformed_data, context={'request': request})

        if (serializer.is_valid()):
            organization = serializer.save()
            retrieval_serializer = serializers.OrganizationRetrievalSerializer(
                organization)
            return Response(retrieval_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationSearchView(APIView):
    """
    Search for organizations by name.

    This view receives a POST request containing a partial or full organization name.
    It returns a list of organizations whose name contains the provided search term.
    If no organizations are found, a message indicating no results is returned.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        organization_name_query = request.data.get(
            'organization_name_query', '')

        if not organization_name_query:
            return Response({"error": "No organization name provided"}, status=400)

        organizations = Organization.objects.filter(
            organization_name__icontains=organization_name_query)

        serializer = serializers.OrganizationRetrievalSerializer(
            organizations, many=True)
        return Response(serializer.data)


class OrganizationDetailView(APIView):
    """
    Retrieve detailed information about an organization, including its associated projects.

    This view expects a POST request with the organization's name slug (`organizationNameSlug`) in the request body.
    It performs the following steps:

    **POST Data**:
        - `organizationNameSlug`: The slug of the organization.

    **Response**:
        - On success: Returns the organization details, including the associated projects, with HTTP status 200.
        - On error: Returns error messages with appropriate HTTP status codes:
            - 400: If the `organizationNameSlug` is missing.
            - 404: If the organization cannot be found.
            - 403: If the user is unauthorized to view the organization.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        organization_name_slug = request.data.get('organizationNameSlug')

        if not organization_name_slug:
            return Response({'error': 'Incomplete credentials provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            organization = Organization.objects.get(
                organization_name_slug=organization_name_slug)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # Only allow members of the organization to view the detail.
        if not organization.members.filter(user=self.request.user).exists():
            return Response({
                "error": "You are unauthorized to view this organization",
                "organization_name": organization.organization_name
            }, status=status.HTTP_403_FORBIDDEN)

        organization_serializer = serializers.OrganizationRetrievalSerializer(
            organization)

        projects = organization.projects.all()
        project_serializer = ProjectRetrievalSerializer(projects, many=True)

        organization_detail = organization_serializer.data
        organization_detail['projects'] = project_serializer.data

        return Response(
            organization_detail, status=status.HTTP_200_OK)


class OrganizationAuthView(APIView):
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
            organization = Organization.objects.get(
                organization_name=organization_name)
        except Organization.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        password = password.strip() if password else None

        if not password:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, organization.organization_password):
            OrganizationMember.objects.create(
                organization=organization, user=self.request.user)
            return Response(status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
