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


class OrganizationAdminRoleRevokeView(generics.UpdateAPIView):
    """
    A view to revoke (remove) an administrator role from a user in a specified organization.
    """

    def put(self, request: Request, *args, **kwargs) -> Response:
        admin_username: str = request.data.get('admin')
        organization_id = kwargs.get('organization_id')

        if not admin_username:
            return Response({'detail': 'Admin username is required.'}, status=status.HTTP_400_BAD_REQUEST)

        organization = self.get_organization(organization_id)
        if not organization:
            return Response({'detail': 'Could not find the organization'}, status=status.HTTP_404_NOT_FOUND)

        admin_user = self.get_user(admin_username)
        if not admin_user:
            return Response({'detail': 'Could not find the user'}, status=status.HTTP_404_NOT_FOUND)

        if not self.is_valid_admin_removal(organization):
            return Response({'detail': 'An organization must have at least one administrator.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not self.user_is_admin_of_organization(request.user, organization):
            return Response({'detail': f'You must be an administrator of {organization.organization_name}\
                              to perform this action.'},
                            status=status.HTTP_400_BAD_REQUEST)

        success, message = self.remove_admin_role(organization, admin_user)
        if not success:
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Admin removed successfully.'}, status=status.HTTP_200_OK)

    def get_organization(self, organization_id) -> Organization:
        try:
            return Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            return None

    def get_user(self, admin_username) -> User | None:
        try:
            return User.objects.get(username=admin_username)
        except User.DoesNotExist:
            return None

    def is_valid_admin_removal(self, organization) -> bool:
        """
        Ensure there is at least 1 admin in the organization
        """
        admins_count = OrganizationMember.objects.filter(
            organization=organization, role=OrganizationMember.ADMIN).count()
        return admins_count > 1

    def user_is_admin_of_organization(self, user, organization) -> bool:
        """
        Check if the user is an admin of the organization
        """
        return OrganizationMember.objects.filter(
            organization=organization, user=user, role=OrganizationMember.ADMIN).exists()

    def remove_admin_role(self, organization, admin_user):
        try:
            admin_member = OrganizationMember.objects.get(
                organization=organization, user=admin_user, role=OrganizationMember.ADMIN)
            admin_member.role = OrganizationMember.MEMBER
            admin_member.save()
            return True, ''
        except OrganizationMember.DoesNotExist:
            return False, 'This user is not an admin of the organization.'
