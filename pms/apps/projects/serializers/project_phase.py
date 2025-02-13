from rest_framework import serializers
from apps.projects import models


class ProjectPhaseSerializer(serializers.ModelSerializer):
    """
    Serializer class for `ProjectPhase` model.
    """

    class Meta:
        model = models.ProjectPhase
        fields = ['phase_id', 'phase_name']


class ProjectPhaseCreateSerializer(serializers.ModelSerializer):
    """
    Handles creation of a custom project phase
    """

    def validate_phase_name(self, phase_name: str) -> str:
        phase_name = phase_name.strip() if phase_name else None

        if not phase_name:
            raise serializers.ValidationError(
                'Please provide a name for your new project workflow')

        return phase_name

    def validate(self, attrs):
        project: models.Project = attrs.get('project')
        phase_name: str = attrs.get('phase_name')

        if models.ProjectPhase.objects.filter(project=project, phase_name__iexact=phase_name).exists():
            raise serializers.ValidationError(
                {
                    'phase_name': 'A project\'s phase name must be unique'
                }
            )

        return attrs

    def create(self, validated_data):
        project: models.Project = validated_data.get('project')
        phase_name: str = validated_data.get('phase_name')

        phase = models.ProjectPhase.objects.create(
            project=project, phase_name=phase_name
        )

        return phase

    class Meta:
        model = models.ProjectPhase
        fields = '__all__'
