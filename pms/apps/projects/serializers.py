from datetime import datetime, timezone
from django.db import transaction
from rest_framework import serializers
from rest_framework.request import Request
from .utils import slugify_project_name
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


class ProjectSerializer(serializers.ModelSerializer):
    """
    `Projects` serializer class.
    """
    class Meta:
        model = models.Project
        fields = ['organization', 'template', 'project_id',
                  'project_name', 'description', 'deadline']

    def validate_description(self, description: str) -> str:
        description = description.strip() if description else ''

        if len(description) > 500:
            raise serializers.ValidationError(
                "Description is too long. Maximum length is 500 characters.")
        return description

    def validate_project_name(self, project_name):
        project_name = project_name.strip() if project_name else None

        if not project_name:
            raise serializers.ValidationError(
                "The project's name is required.")

        length = len(project_name)
        if length < 5 or length > 60:
            raise serializers.ValidationError(
                "A project's name must be between 5 and 60 characters long.")

        return project_name

    def validate_deadline(self, deadline: str) -> str:
        if deadline < datetime.now(timezone.utc).date():
            raise serializers.ValidationError(
                "Deadline cannot be in the past.")

        return deadline

    def validate(self, attrs):
        organization = attrs.get('organization')
        project_name = attrs.get('project_name')

        if organization.projects.filter(project_name__iexact=project_name).exists():
            raise serializers.ValidationError({
                'project_name': 'A project with this name already exists in the organization.'
            })

        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        request: Request = self.context.get('request')
        template = validated_data.get('template')
        deadline = validated_data.get('deadline')
        organization = validated_data.get('organization')
        project_name = validated_data.get('project_name')
        description = validated_data.get('description')
        project_name_slug = slugify_project_name(project_name)

        if template:
            project = models.Project.objects.create(organization=organization, template=template,
                                                    project_name=project_name, project_name_slug=project_name_slug,
                                                    description=description, deadline=deadline)
        else:
            project = models.Project.objects.create(organization=organization,
                                                    project_name=project_name, project_name_slug=project_name_slug,
                                                    description=description, deadline=deadline)

        models.ProjectMember.objects.create(
            member=request.user, project=project)

        if template:
            template_phases = [models.ProjectPhase(
                project=project, template_phase=phase) for phase in template.phases.all()]
            models.ProjectPhase.objects.bulk_create(template_phases)

        return project


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
