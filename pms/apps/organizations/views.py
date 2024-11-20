from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Organization, OrganizationMembers
from .serializers import OrganizationSerializer

# Create your views here.


class UserOrganizationListView(APIView):
    """
    Displays a list of organizations that the currently authenticated user
    is a member of.
    """
    model = Organization

    def get(self, request) -> Response:
        # Get all OrganizationMembers entries where the user is a member
        user_organizations = OrganizationMembers.objects.filter(
            user=self.request.user)

        # Get the related Organization objects for those memberships
        organizations = Organization.objects.filter(
            organization_id__in=user_organizations.values('organization_id')
        )

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)
