from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.users.models import User
from apps.users.serializers import UserRetrievalSerializer
from apps.projects import models


class ProjectMembersListView(generics.ListAPIView):
    """
    Returns a list of members of a project.
    """

    serializer_class = UserRetrievalSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')

        if not project_id:
            raise ValidationError({'detail': 'No project was provided.'})

        project = get_object_or_404(models.Project, pk=project_id)

        memberships = project.members.all()
        members = [membership.member for membership in memberships]
        return members


class NonProjectMemberListView(generics.ListAPIView):
    """
    Returns a list of users who are members of an organization
    but not members of the project.
    """

    serializer_class = UserRetrievalSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')

        if not project_id:
            raise ValidationError(
                {'detail': 'No project was provided'})

        project = get_object_or_404(models.Project, pk=project_id)

        organization_members = User.objects.filter(
            organizationmember__organization=project.organization)

        project_members = models.ProjectMember.objects.filter(
            project=project).values_list('member_id', flat=True)

        non_project_members = organization_members.exclude(
            user_id__in=project_members)

        return non_project_members


class ProjectMemberAdditionView(generics.CreateAPIView):
    """
    Handles request from project managers to add members to a 
    project.

    This view expects a POST request with a list of usernames.
    """

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        usernames: list[str] = request.data.get('members')

        if not usernames:
            return Response({'detail': 'No members to be added were provided'}, status=status.HTTP_400_BAD_REQUEST)

        project_id = self.kwargs.get('project_id')

        username_set = set(usernames)

        users = User.objects.filter(username__in=username_set)

        project = get_object_or_404(models.Project, pk=project_id)

        models.ProjectMember.objects.bulk_create(
            [
                models.ProjectMember(project=project, member=user)
                for user in users
            ]
        )

        return Response(status=status.HTTP_201_CREATED)
