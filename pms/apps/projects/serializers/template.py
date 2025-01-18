from django.db import transaction
from rest_framework import serializers
from apps.projects import models
from apps.projects.serializers import IndustrySerializser


class TemplateSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `Template` model. This class is used by the API to 
    create temlates.
    """
    class Meta:
        model = models.Template
        fields = ['industry', 'template_name']

    def validate_template_name(self, template_name: str) -> str:
        template_name = template_name.strip() if template_name else None

        if not template_name:
            raise serializers.ValidationError("Template name cannot be empty.")

        if len(template_name) > 50:
            raise serializers.ValidationError(
                "Template name must be 50 characters or below.")

        return template_name

    def validate(self, attrs):
        industry = attrs.get("industry")
        template_name = attrs.get("template_name")
        template_phases = self.context.get('template_phases')

        template_phases = list(
            filter(None, map(str.strip, template_phases))) if template_phases else None

        # Check if a template with the same name already exists in the industry
        if industry.templates.filter(template_name__iexact=template_name).exists():
            raise serializers.ValidationError(
                {
                    "template_name": "A template with that name already exists in the industry."
                }
            )

        # Validate that the template has a workflow.
        if not template_phases:
            raise serializers.ValidationError(
                "A template must have a workflow."
            )

        # Update context with the validated template workflow.
        self.context['template_phases'] = template_phases

        # Check if a template with the same phases exists in the industry
        industry_templates = industry.templates.prefetch_related("phases")
        for template in industry_templates:
            existing_phases = template.phases.values_list(
                "phase_name", flat=True)
            if set(template_phases) == set(existing_phases):
                raise serializers.ValidationError(
                    {
                        "template_phases": "Another template in the selected industry has the same workflow."
                    }
                )

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        industry = validated_data.get("industry")
        template_name = validated_data.get("template_name")
        template_phases = self.context.get('template_phases')

        # Create the template
        template = models.Template.objects.create(
            industry=industry,
            template_name=template_name,
        )

        # Create the template phases
        models.TemplatePhase.objects.bulk_create([
            models.TemplatePhase(template=template, phase_name=phase_name)
            for phase_name in template_phases
        ])

        return template


class TemplateSearchSerializer(serializers.ModelSerializer):
    """
    TemplateSearchSerializer

    This serializer is used to serialize template instances along with their associated
    industries when performing a search for a template to use in a project. 
    It utilizes the IndustrySerializer to handle the serialization of the related industry data. 
    """
    industry = IndustrySerializser()

    class Meta:
        model = models.Template
        fields = '__all__'


class TemplatePhaseSerializer(serializers.ModelSerializer):
    """
    Serializer class for `TemplatePhase` model.
    """
    class Meta:
        model = models.TemplatePhase
        fields = ['phase_name']
