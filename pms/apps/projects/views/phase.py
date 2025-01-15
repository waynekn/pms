from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.tasks.models import Task
from apps.tasks.serializers import TaskRetrievalSerializer
from apps.projects import models, serializers


class ProjectPhaseRetrieveView(generics.RetrieveAPIView):
    """
    Retrieves all the phases of a project.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        project_id = self.kwargs.get('project_id')

        if not project_id:
            return Response({'detail': 'No project was provided.'}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(models.Project, pk=project_id)

        project_data = serializers.ProjectRetrievalSerializer(project).data

        project_phases = project.phases.all()

        serializer = serializers.ProjectPhaseSerializer(
            project_phases, many=True)

        project_data['phases'] = serializer.data

        return Response(project_data, status=status.HTTP_200_OK)


class ProjectPhaseDetailView(generics.RetrieveAPIView):
    """
    Retrieve detailed information about a specific ProjectPhase.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        phase_id = kwargs.get('phase_id')

        project_phase: models.ProjectPhase = get_object_or_404(
            models.ProjectPhase, pk=phase_id)

        project = project_phase.project

        try:
            membership = models.ProjectMember.objects.get(
                project=project, member=self.request.user)
        except models.ProjectMember.DoesNotExist:
            return Response({'detail': 'You are not authorized to access this information'},
                            status=status.HTTP_403_FORBIDDEN)

        in_progress_tasks = Task.objects.filter(
            project_phase=project_phase, status=Task.IN_PROGRESS)
        on_hold_tasks = Task.objects.filter(
            project_phase=project_phase, status=Task.ON_HOLD)
        done_tasks = Task.objects.filter(
            project_phase=project_phase, status=Task.DONE)

        detail = {
            "project": serializers.ProjectRetrievalSerializer(project).data,
            "phase": serializers.ProjectPhaseSerializer(project_phase).data,
            'role': membership.role,
            "in_progress": TaskRetrievalSerializer(in_progress_tasks, many=True).data,
            "on_hold": TaskRetrievalSerializer(on_hold_tasks, many=True).data,
            "completed": TaskRetrievalSerializer(done_tasks, many=True).data,
        }

        return Response(detail, status=status.HTTP_200_OK)


class CustomProjectPhaseCreateView(generics.CreateAPIView):
    """
    Handle requests to create a custom project phase.

    This view expects a dict, with a name key, which will be the
    name of the new project phase
    """

    serializer_class = serializers.CustomPhaseCreateSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        project_id = kwargs.get('project_id')
        phase_name = request.data.get('name')

        if not phase_name:
            return Response({'detail': 'Please provide a name for your new project workflow.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            project = models.Project.objects.get(pk=project_id)
        except models.Project.DoesNotExist:
            return Response({'detail': 'Could not get the project.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            membership = models.ProjectMember.objects.get(
                project=project, member=self.request.user)
        except models.ProjectMember.DoesNotExist:
            return Response({'detail': 'You are not authorized to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)

        if membership.role != 'Manager':
            return Response({'detail': 'You are not authorized to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)

        data = {
            'project': project_id,
            'phase_name': phase_name
        }
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            phase = serializer.save()
            phase = serializers.CustomPhaseRetrievalSerializer(phase).data

            return Response(phase, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
