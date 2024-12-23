from django.db import transaction
from rest_framework import serializers
from . import models


class IndustrySerializser(serializers.ModelSerializer):
    """
    A serializer class for the `Industry` model. This class is used by the API to serialize 
    `Industry` instances into JSON data before returning it to the client.

    Attributes:
        Meta (class): A class containing metadata for the serializer.
    """
    class Meta:
        model = models.Industry
        fields = ['industry_id', 'industry_name']


class TemplateSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `Template` model. This class is used by the API to serialize 
    `Template` instances into JSON data before returning it to the client.

    Attributes:
        Meta (class): A nested class containing metadata for the serializer.
    """
    class Meta:
        model = models.Template
        fields = ['industry', 'template_name']

    def validate_template_name(self, template_name: str) -> str:
        template_name = template_name.strip() if template_name else None

        if not template_name:
            raise serializers.ValidationError("Template name cannot be empty.")

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
