from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.response import Response

from apps.organizations import models


class OrgnizationMemberDeleteView(generics.DestroyAPIView):
    """
    A view for handling the deletion of a user's membership in an organization.

    This view allows a user to exit an organization they are a member of.
    """

    def delete(self, request: Request, *args, **kwargs) -> Response:
        org_id = kwargs.get('organization_id')

        # get the organization
        try:
            organization = models.Organization.objects.get(pk=org_id)
        except models.Organization.DoesNotExist:
            return Response({'detail': 'Could not get the organization'},
                            status=status.HTTP_404_NOT_FOUND)

        # get the organization membership
        try:
            membership = models.OrganizationMember.objects.get(
                organization=organization, user=request.user)
        except models.Organization.DoesNotExist:
            return Response({'detail': 'You are not a member of this organization'},
                            status=status.HTTP_400_BAD_REQUEST)

        # ensure an organization must have at least 1 admin
        if membership.role == models.OrganizationMember.ADMIN:
            org_admins_count = models.OrganizationMember.objects.filter(organization=organization,
                                                                        role=models.OrganizationMember.ADMIN).count()

            if org_admins_count <= 1:
                return Response({'detail': 'An organization must have at least 1 administrator'},
                                status=status.HTTP_400_BAD_REQUEST)

        membership.delete()

        return Response({'detail': f'You are no longer a member of {organization.organization_name}'},
                        status=status.HTTP_200_OK)
