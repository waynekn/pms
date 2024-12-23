import datetime
from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from apps.organizations.models import Organization
from .models import Project, Template


class ProjectCreateForm(forms.ModelForm):
    """
    Form for creating a new Project. This form includes fields for the template,
    project name, description, and deadline.
    """

    class Meta:
        model = Project
        fields = ['organization', 'template',
                  'project_name', 'description', 'deadline']

        widgets = {
            'organization': forms.TextInput(attrs={'readonly': 'readonly'}),
            'template': forms.HiddenInput(),
            'project_name': forms.TextInput(attrs={'placeholder': 'Enter project name', 'maxlength': '120'}),
            'description': forms.Textarea(attrs={'placeholder': 'Provide a description of the project (Optional)'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Get 'organization_name_slug' that was passed from ProjectCreateView.
        organization_name_slug = kwargs.pop("organization_name_slug", None)
        super().__init__(*args, **kwargs)

        organization = get_object_or_404(
            Organization, organization_name_slug=organization_name_slug)
        self.initial['organization'] = organization
        super().__init__(*args, **kwargs)

    def clean_template(self):
        template_id = self.cleaned_data["template"]

        try:
            return Template.objects.get(pk=template_id)
        except Template.DoesNotExist:
            raise ValidationError("Could not get the template.")

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < datetime.datetime.now():
            raise ValidationError('Deadlines must be in the future.')
        return deadline

    def clean(self):
        cleaned_data = super().clean()
        organization = cleaned_data.get("organization")
        project_name = cleaned_data.get('project_name')

        if organization.projects.filter(project_name=project_name).exists():
            self.add_error(
                'project_name', 'A project with that name already exists in the organization')

        return cleaned_data
