from datetime import datetime, timezone
from rest_framework import serializers

from apps.projects.models import ProjectPhase
from apps.projects.serializers import ProjectPhaseSerializer
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


class TaskRetrievalSerializer(serializers.ModelSerializer):
    project_phase = ProjectPhaseSerializer()

    class Meta:
        model = models.Task
        exclude = ['project']
