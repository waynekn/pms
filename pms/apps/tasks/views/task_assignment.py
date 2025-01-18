from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.tasks import models
from apps.tasks import serializers
from apps.users.models import User
from apps.projects.models import ProjectMember
from apps.users.serializers import UserRetrievalSerializer


class TaskAssignmentView(generics.CreateAPIView):
    """
    View to handle the assignment of users to a task.

    This endpoint allows users to be assigned to a specific task.
    """
    serializer_class = serializers.TaskAssignMentSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        task_id = self.kwargs.get('task_id')

        try:
            task = models.Task.objects.get(pk=task_id)
        except models.Task.DoesNotExist:
            return Response({'detail': 'Could not get the task'}, status=status.HTTP_404_NOT_FOUND)

        try:
            membership = ProjectMember.objects.get(
                project=task.project, member=self.request.user)
        except ProjectMember.DoesNotExist:
            return Response({'detail': 'You are unauthorized to access this information.'},
                            status=status.HTTP_403_FORBIDDEN)

        if membership.role != 'Manager':
            return Response({'detail': 'You are unauthorized to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)

        data = {
            'task_id': task_id,
            'usernames': request.data.get('assignees') or []
        }

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NonTaskAssigneesListView(generics.ListAPIView):
    """
    Retrieves a list of users who are members of a project but have not been
    assigned to a specific task.

    The response will be a list of users who are project members but not 
    task assignees.
    """

    serializer_class = UserRetrievalSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')

        try:
            task = models.Task.objects.get(pk=task_id)
        except models.Task.DoesNotExist:
            raise ValidationError({'detail': 'Could not get the task.'})

        project = task.project

        task_assignments = set(models.TaskAssignment.objects.filter(
            task_id=task_id).values_list('user', flat=True))

        memberships = ProjectMember.objects.filter(
            project=project).values_list('member', flat=True)

        # Exclude users who are assigned to the task
        non_assignees_ids = [
            member for member in memberships if member not in task_assignments]

        return User.objects.filter(user_id__in=[non_assignees_id for non_assignees_id in non_assignees_ids])
