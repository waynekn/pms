from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response


from pms.utils import camel_case_to_snake_case

from apps.projects.models import ProjectMember, ProjectPhase
from apps.tasks import serializers
from apps.tasks import models


class TaskCreateView(generics.CreateAPIView):
    """
    View for creating a new task.

    This view handles POST requests for creating a new task.
    """
    model = models.Task
    serializer_class = serializers.TaskCreationSerializser

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        transformed_data = camel_case_to_snake_case(data)

        project_phase: str = transformed_data.get('project_phase')

        try:
            project_phase = ProjectPhase.objects.get(pk=project_phase)
        except ProjectPhase.DoesNotExist:
            return Response({'project_phase': ['Could not get the phase of the project']},
                            status=status.HTTP_404_NOT_FOUND)

        project = project_phase.project

        try:
            membership = ProjectMember.objects.get(
                project=project, member=self.request.user)
        except ProjectMember.DoesNotExist:
            return Response({'non_field_errors': ['You are not authorized to perform this action.']},
                            status=status.HTTP_403_FORBIDDEN)

        if membership.role != 'Manager':
            return Response({'non_field_errors': ['You are not authorized to perform this action.']},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=transformed_data)

        if serializer.is_valid():
            task = serializer.save()
            serialized_task = serializers.TaskRetrievalSerializer(task)
            return Response(serialized_task.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
