from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.projects import models, serializers

from apps.tasks.serializers import TaskRetrievalSerializer


class ProjectTasksView(APIView):
    """
    Returns all the tasks related to a project.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        project_id = self.kwargs.get('project_id')

        if not project_id:
            return Response({'detail': 'No project was provided.'}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(models.Project, pk=project_id)

        project_detail = serializers.ProjectRetrievalSerializer(project).data

        tasks = project.tasks.all()

        tasks_data = TaskRetrievalSerializer(tasks, many=True).data

        project_detail['tasks'] = tasks_data

        return Response(project_detail, status=status.HTTP_200_OK)
