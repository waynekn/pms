from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from apps.projects.serializers import ProjectRetrievalSerializer
from apps.organizations.models import Organization, OrganizationMember
from apps.organizations import serializers


class OrganizationDetailView(generics.RetrieveAPIView):
    """
    Retrieve detailed information about an organization, including its associated projects.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        organization_name_slug = kwargs.get('organization_name_slug')

        try:
            organization = Organization.objects.get(
                organization_name_slug=organization_name_slug)
        except Organization.DoesNotExist:
            return Response({'detail': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # Only allow members of the organization to view the detail.
        try:
            membership = OrganizationMember.objects.get(
                organization=organization, user=self.request.user)
        except OrganizationMember.DoesNotExist:
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
        organization_detail['role'] = membership.role

        return Response(
            organization_detail, status=status.HTTP_200_OK)
