from typing import Any
from rest_framework import status
from rest_framework import generics
from django.views.generic import DetailView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from pms.utils import camel_case_to_snake_case
from .models import Organization, OrganizationMember
from .serializers import OrganizationSerializer

# Create your views here.


class UserOrganizationListView(APIView):
    """
    Displays a list of organizations that the currently authenticated user
    is a member of.
    """
    model = Organization

    def get(self, request) -> Response:
        # Get all OrganizationMember entries where the user is a member
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user)

        # Get the related Organization objects for those memberships
        organizations = Organization.objects.filter(
            organization_id__in=user_organizations.values('organization_id')
        )

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)


class OrganizationCreateView(generics.CreateAPIView):
    """
    Creates an organization, saves it to the database and adds the
    user who creates the organization to its members.
    """
    model = Organization
    serializer_class = OrganizationSerializer

    def post(self, request, *args, **kwargs):
        transformed_data = camel_case_to_snake_case(request.data)
        serializer = self.get_serializer(
            data=transformed_data, context={'request': request})

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)


class OrganizationDetailView(DetailView):
    model = Organization
    context_object_name = 'organization'
    slug_field = 'organization_name_slug'
    slug_url_kwarg = 'organization_name_slug'
    template_name = "organizations/organization_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        organization = self.get_object()
        context["projects"] = organization.projects.all()
        return context
