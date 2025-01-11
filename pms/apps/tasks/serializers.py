from datetime import datetime, timezone
from django.db import transaction
from rest_framework import serializers

from apps.projects.models import ProjectPhase
from apps.projects.serializers import ProjectPhaseSerializer
from apps.users.models import User
from . import models


class TaskCreationSerializser(serializers.ModelSerializer):

    def validate_task_name(self, task_name: str) -> str:
        task_name = task_name.strip() if task_name else None

        if not task_name:
            raise serializers.ValidationError('This field is required.')

        if len(task_name) < 5 or len(task_name) > 30:
            raise serializers.ValidationError(
                'The length of is out of bounds. It must be between 5 and 30 characters long.')

        return task_name

    def validate_deadline(self, deadline: datetime.date) -> datetime.date:
        """
        Validate deadline is in the future.
        """

        if deadline < datetime.now(timezone.utc).date():
            raise serializers.ValidationError(
                "The deadline of a task must be in the future.")

        return deadline

    def validate_description(self, description: str) -> str:
        """
        Validate description is not too long.
        """

        description = description.strip() if description else None

        if not description:
            raise serializers.ValidationError(
                'Please provide a description for your task.')

        if len(description) > 500:
            raise serializers.ValidationError(
                "Description is too long. It must be 500 or less characters")

        return description

    def validate(self, attrs):
        project_phase: ProjectPhase = attrs.get('project_phase')
        task_name: str = attrs.get('task_name')

        if task_name and project_phase.phase_tasks.filter(task_name__iexact=task_name).exists():
            raise serializers.ValidationError({
                'task_name': 'A task with this name already exists in this phase.'
            })

        return attrs

    def create(self, validated_data):
        project_phase: ProjectPhase = validated_data.get('project_phase')
        task_name = validated_data.get('task_name')
        description = validated_data.get('description')
        deadline = validated_data.get('deadline')

        project = project_phase.project

        return models.Task.objects.create(
            project=project,
            project_phase=project_phase,
            task_name=task_name,
            description=description,
            deadline=deadline,
        )

    class Meta:
        model = models.Task
        fields = ['project_phase', 'task_name',
                  'deadline', 'description']


class TaskAssignMentSerializer(serializers.Serializer):
    """
    Serializer for assigning users to a task.
    This serializer is used to validate and save task assignments.
    """
    usernames = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    task_id = serializers.CharField(write_only=True)

    def validate(self, data):
        task_id = data.get('task_id')
        try:
            task = models.Task.objects.get(pk=task_id)
        except models.Task.DoesNotExist:
            raise serializers.ValidationError(
                {'task_id': 'Task does not exist.'})

        data['task'] = task

        usernames = data.get('usernames')
        users = User.objects.filter(username__in=usernames)
        if not users.exists():
            raise serializers.ValidationError(
                {'usernames': 'No valid users found.'})

        data['users'] = users
        return data

    @transaction.atomic
    def create(self, validated_data):
        task = validated_data['task']
        users = validated_data['users']

        # Avoid duplicate assignments
        existing_assignments = models.TaskAssignment.objects.filter(
            task=task, user__in=users
        ).values_list('user_id', flat=True)
        new_assignments = [
            models.TaskAssignment(task=task, user=user)
            for user in users if user.user_id not in existing_assignments
        ]

        models.TaskAssignment.objects.bulk_create(
            new_assignments, ignore_conflicts=True)

        return {'task': task, 'assigned_users': [user.username for user in users]}


class TaskRetrievalSerializer(serializers.ModelSerializer):
    project_phase = ProjectPhaseSerializer()

    class Meta:
        model = models.Task
        exclude = ['project']
