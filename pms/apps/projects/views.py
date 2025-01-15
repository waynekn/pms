from uuid import UUID
from django.db import transaction
from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from . import models
from . import serializers
from apps.tasks.models import Task
from apps.organizations.models import OrganizationMember
from apps.users.serializers import UserRetrievalSerializer
from apps.tasks.serializers import TaskRetrievalSerializer
from apps.users.models import User
from pms.utils import camel_case_to_snake_case


class IndustryListView(generics.ListAPIView):
    """
    A view that returns a list of all industries in the system. This view is used by the 
    frontend to populate the industry dropdown when creating a new template.

    Attributes:
        queryset (QuerySet): A queryset containing all industries in the system.
        serializer_class (Serializer): The serializer class used to serialize the industries.
    """
    queryset = models.Industry.objects.all()
    serializer_class = serializers.IndustrySerializser


class TemplateCreateView(generics.CreateAPIView):
    """
    A view to handle the creation of a new Template resource.

    This view accepts a POST request with the data for a new template, processes
    the `TemplateCreateForm` data (transformed to snake_case), and creates a 
    `Template` instance along with its associated `TemplatePhase` instances. 
    If the form is valid, the new template and phases are saved to the database 
    and a successful response with the created template data is returned. 
    If the form is invalid, a 400 Bad Request response with errors is returned.

    Attributes:
        model (class): The model associated with this view, `Template`.
        serializer_class (class): The serializer class used for serializing
                                  template data, `TemplateSerializer`.

    """
    model = models.Template
    serializer_class = serializers.TemplateSerializer

    def post(self, request, *args, **kwargs):
        transformed_data = camel_case_to_snake_case(request.data)
        serializer = self.get_serializer(
            data=transformed_data, context={'request': request, 'template_phases': transformed_data.get('template_phases')})

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCreateView(generics.CreateAPIView):
    """
    A view that handles the creation of a new project.

    This view accets a POST request with the data with the following data necessary
    to create a project: 
    - organization,project name, template(optional), description and deadline

    Upon successful validation, the new project instance is created, and a `201 Created` 
    response with the serialized data of the project is returned.
    If validation fails, a `400 Bad Request` response with error details is returned.

    Attributes:
        model (models.Project): The model associated with this view, which is `Project`.
        serializer_class (serializers.ProjectCreationSerializer): The serializer used to validate and
            serialize the project data.
    """
    model = models.Project
    serializer_class = serializers.ProjectCreationSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        transformed_data = camel_case_to_snake_case(request.data)
        serializer = self.get_serializer(
            data=transformed_data, context={'request': request}
        )
        organization_id: UUID = transformed_data.get('organization')

        if not organization_id:
            return Response({'organization': ['This field is required']},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            membership = OrganizationMember.objects.get(
                organization_id=organization_id, user=self.request.user)
        except OrganizationMember.DoesNotExist:
            # Dont allow a person who is not a member of the organization to create a project.
            return Response({
                'non_field_errors': ['You must be a member of the organization to create a project']},
                status=status.HTTP_400_BAD_REQUEST)

        if membership.role != 'Admin':
            return Response({
                'non_field_errors': ['You dont have the necessary permissions to \
                 create a project for this organization']},
                status=status.HTTP_400_BAD_REQUEST)

        if (serializer.is_valid()):
            project = serializer.save()
            project_retrieval_serializer = serializers.ProjectRetrievalSerializer(
                project)
            return Response(project_retrieval_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectStatsView(APIView):
    """
    Handles requests to get a project's statistics.

    This view expects a GET request with a pk query parameter.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        pk = request.query_params.get('pk')

        if not pk:
            return Response({'detail': 'No project was provided'}, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(models.Project, pk=pk)

        task_counts = project.tasks.aggregate(
            total_tasks=Count('task_id'),
            in_progress=Count(
                Case(When(status='IN_PROGRESS', then=1), output_field=IntegerField())),
            on_hold=Count(Case(When(status='ON_HOLD', then=1),
                          output_field=IntegerField())),
            completed=Count(
                Case(When(status='COMPLETED', then=1), output_field=IntegerField())),
        )

        total_tasks = task_counts['total_tasks']
        completed_tasks = task_counts['completed']

        stats = {
            'tasks': total_tasks,
            'members': project.members.count(),
            'description': project.description,
            'tasks_in_progress': task_counts['in_progress'],
            'tasks_on_hold': task_counts['on_hold'],
            'tasks_completed': task_counts['completed'],
            'percentage_completion': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        }

        return Response(stats, status=status.HTTP_200_OK)


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


class UserProjectsListView(generics.ListAPIView):
    """
    Returns all the projects that the user is a member of.
    """
    serializer_class = serializers.ProjectRetrievalSerializer

    def get_queryset(self):
        memberships = self.request.user.projects.all()
        projects = [membership.project for membership in memberships]
        return projects


class TemplateSearchView(generics.ListAPIView):
    """
    Handles searching for a template by name.
    """

    serializer_class = serializers.TemplateSearchSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        name = name.strip() if name else None

        if not name:
            return []

        return models.Template.objects.filter(
            template_name__icontains=name)
