from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.users.models import User
from apps.projects.models import ProjectMember, ProjectPhase
from apps.users.serializers import UserRetrievalSerializer
from pms.utils import camel_case_to_snake_case

from . import serializers
from . import models


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


class TaskStatusUpdateView(generics.UpdateAPIView):
    """
    Handles updating of a task status.

    This view expects a POST request with a status key whose value
    is potentially the new task status.
    """

    def put(self, request: Request, *args, **kwargs) -> Response:
        new_status = request.data.get('status')
        task_id = kwargs.get('task_id')

        if not hasattr(models.Task, new_status):
            return Response({"detail": "Invalid status choice. Status must either be \
                             'IN_PROGRESS', 'ON_HOLD' or 'DONE"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = models.Task.objects.get(pk=task_id)
        except models.Task.DoesNotExist:
            return Response({"detail": "Could not get task"}, status=status.HTTP_404_NOT_FOUND)

        task.status = new_status

        task.save()

        return Response(status=status.HTTP_200_OK)
