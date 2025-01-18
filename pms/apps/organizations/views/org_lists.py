from rest_framework import generics

from apps.organizations.models import Organization, OrganizationMember
from apps.organizations import serializers


class OrganizationSearchView(generics.ListAPIView):
    """
    Search for organizations by name.
    """

    serializer_class = serializers.OrganizationRetrievalSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')

        name = name.strip() if name else None

        if not name:
            return []

        return Organization.objects.filter(
            organization_name__icontains=name)


class UserOrganizationListView(generics.ListAPIView):
    """
    Displays a list of organizations that the currently authenticated user
    is a member of.
    """
    serializer_class = serializers.OrganizationRetrievalSerializer

    def get_queryset(self):
        user_organizations = OrganizationMember.objects.filter(
            user=self.request.user)

        # Get the related Organization objects for those memberships
        return Organization.objects.filter(
            organization_id__in=user_organizations.values('organization_id')
        )
