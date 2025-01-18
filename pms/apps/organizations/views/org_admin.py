from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.users.serializers import UserRetrievalSerializer
from apps.users.models import User
from apps.organizations.models import Organization, OrganizationMember


class OrganizationAdminsListView(generics.ListAPIView):
    """
    Returns a list of users who are organization administrators.
    """
    serializer_class = UserRetrievalSerializer

    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')

        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            raise ValidationError('Could not get the organization.')

        admins = OrganizationMember.objects.filter(
            organization=organization, role='Admin').values_list('user', flat=True)

        return User.objects.filter(user_id__in=admins)


class NonOrganizationAdminsListView(generics.ListAPIView):
    """
    Returns a list of users who are members of an organization
    but are not organization administrators.
    """
    serializer_class = UserRetrievalSerializer

    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')

        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            raise ValidationError('Could not get the organization.')

        admins = OrganizationMember.objects.filter(
            organization=organization, role='Member').values_list('user', flat=True)

        return User.objects.filter(user_id__in=admins)


class OrganizationAdminCreateView(generics.ListCreateAPIView):
    """
    Assigns members administration privilleges for an organization.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        organization_id = kwargs.get('organization_id')
        members: list[str] = request.data.get('members')

        if not members:
            return Response({'detail': 'No organization members to be added were provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return Response({'detail': 'No organization matches the given query'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            membership = OrganizationMember.objects.get(
                organization=organization, user=self.request.user)
        except OrganizationMember.DoesNotExist:
            return Response({'detail': 'You dont have the necessary permissions to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)

        if membership.role != 'Admin':
            return Response({'detail': 'You dont have the necessary permissions to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)

        users = User.objects.filter(username__in=members)

        org_members = OrganizationMember.objects.filter(
            organization=organization, user__in=users)

        for member in org_members:
            member.role = 'Admin'
            member.save()

        return Response(status=status.HTTP_200_OK)
