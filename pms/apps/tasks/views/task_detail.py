from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from apps.tasks import models
from apps.tasks import serializers
from apps.users.models import User
from apps.projects.models import ProjectMember
from apps.users.serializers import UserRetrievalSerializer


class TaskDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a task detail.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        task_id = kwargs.get('task_id')

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

        task_data = serializers.TaskRetrievalSerializer(task).data

        user_ids = models.TaskAssignment.objects.filter(
            task_id=task_id).values_list('user', flat=True)

        users = User.objects.filter(user_id__in=user_ids)

        assignees = UserRetrievalSerializer(users, many=True).data

        task_data['assignees'] = assignees
        task_data['role'] = membership.role

        return Response(task_data, status=status.HTTP_200_OK)
