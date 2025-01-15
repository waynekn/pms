from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.projects import models


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
                Case(When(status='DONE', then=1), output_field=IntegerField())),
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
