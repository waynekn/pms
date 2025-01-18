from rest_framework import serializers
from apps.projects import models
from apps.projects.serializers import (
    TemplatePhaseSerializer,
)


class CustomPhaseRetrievalSerializer(serializers.ModelSerializer):
    """
    Handles retreival of a custom project phase
    """

    class Meta:
        model = models.CustomPhase
        fields = ['phase_id', 'phase_name']


class ProjectPhaseSerializer(serializers.ModelSerializer):
    """
    Serializer class for `ProjectPhase` model.
    """
    template_phase = TemplatePhaseSerializer()
    custom_phase = CustomPhaseRetrievalSerializer()

    class Meta:
        model = models.ProjectPhase
        fields = ['phase_id', 'template_phase', 'custom_phase']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.template_phase:
            representation['phase_name'] = instance.template_phase.phase_name
        elif instance.custom_phase:
            representation['phase_name'] = instance.custom_phase.phase_name

        representation.pop('template_phase', None)
        representation.pop('custom_phase', None)

        return representation


class CustomPhaseCreateSerializer(serializers.ModelSerializer):
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

        if project.template:
            if (models.CustomPhase.objects.filter(project=project, phase_name__iexact=phase_name).exists() or
                    project.template.phases.filter(phase_name__iexact=phase_name).exists()):
                raise serializers.ValidationError(
                    {
                        'phase_name': 'A project\'s phase name must be unique'
                    }
                )
        else:
            if models.CustomPhase.objects.filter(project=project, phase_name__iexact=phase_name).exists():
                raise serializers.ValidationError(
                    {
                        'phase_name': 'A project\'s phase name must be unique'
                    }
                )

        return attrs

    def create(self, validated_data):
        project: models.Project = validated_data.get('project')
        phase_name: str = validated_data.get('phase_name')

        phase = models.CustomPhase.objects.create(
            project=project, phase_name=phase_name
        )

        models.ProjectPhase.objects.create(
            project=project, custom_phase=phase
        )

        return phase

    class Meta:
        model = models.CustomPhase
        fields = '__all__'
