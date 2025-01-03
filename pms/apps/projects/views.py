from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from . import models
from . import serializers
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
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectStatsView(APIView):
    """
    Handles requests to get a project's statistics.

    This view expects a GET request with a pk query parameter.
    """

    def get(self, request: Request, *args, **kwargs) -> Response:
        pk = request.query_params.get('pk')

        if not pk:
            return Response({'error': 'No project was provided'}, status=status.HTTP_400_BAD_REQUEST)

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


class TemplateSearchView(APIView):
    """
    Handles searching for a template by name.

    This view accepts a POST request with a JSON payload containing a `name` key.
    It returns a JSON response with a list of templates that match the provided name,
    along with their associated industries.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        searchstr = request.data.get('name')

        searchstr = searchstr.strip() if searchstr else None

        if not searchstr:
            return Response([], status=status.HTTP_200_OK)

        templates = models.Template.objects.filter(
            template_name__icontains=searchstr)

        serializer = serializers.TemplateSearchSerializer(
            templates, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
