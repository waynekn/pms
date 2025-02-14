from datetime import datetime, timezone
from django.db import transaction
from rest_framework import serializers
from rest_framework.request import Request
from apps.organizations.serializers import OrganizationRetrievalSerializer
from apps.projects.utils.slugs import slugify_project_name
from apps.projects import models


class ProjectCreationSerializer(serializers.ModelSerializer):
    """
    `Project` creation serializer class.
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
            member=request.user, project=project, role='Manager')

        if template:
            template_phases = [models.ProjectPhase(
                project=project, phase_name=phase.phase_name) for phase in template.phases.all()]
            models.ProjectPhase.objects.bulk_create(template_phases)

        return project


class ProjectRetrievalSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving project data.
    """
    organization = OrganizationRetrievalSerializer()

    class Meta:
        model = models.Project
        exclude = ['template',]
