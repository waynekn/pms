import datetime
from typing import Any
from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from apps.organizations.models import Organization
from .models import Industry, Project, Template


class TemplateCreateForm(forms.Form):
    """
    A form used for creating a new template in the system. It collects information about 
    the template name, associated industry, and template phases. The form validates that the 
    template name is unique within the chosen industry and that the template phases are not 
    duplicated across other templates within the same industry.

    Attributes:
        industry_choice (ModelChoiceField): A choice field for selecting an industry. 
                                            It pulls data from the `Industry` model.
        template_name (CharField): A field for entering the template name. 
                                   The name must be unique within the selected industry.
        template_phases (CharField): A hidden field containing a comma-separated list of 
                                      phases associated with the template.

    Methods:
        clean_template_name(): Validates the template name ensuring it is not empty or whitespace.
        clean_template_phases(): Ensures that the template phases field is not empty.
        clean(): Validates that no other template within the same industry has identical phases 
                 and that the template name is unique within the selected industry.
    """
    industry_choice = forms.ModelChoiceField(
        queryset=Industry.objects.all(), label="industry", required=True)
    template_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter template name'}),
        max_length=50, label="template_name", required=True)
    template_phases = forms.CharField(widget=forms.HiddenInput(),
                                      required=True,
                                      label="template_phases"
                                      )

    def clean_template_name(self):
        template_name = self.cleaned_data["template_name"]

        if not template_name or not template_name.strip():
            raise ValidationError("Template name cannot be empty.")

        return template_name.strip()

    def clean_template_phases(self) -> str:
        template_phases = self.cleaned_data["template_phases"]

        if not template_phases:
            raise ValidationError("Phases cannot be empty.")

        return template_phases

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        template_phases = cleaned_data.get("template_phases")
        industry = cleaned_data.get("industry_choice")
        template_name = cleaned_data.get("template_name")

        if not industry:
            self.add_error("industry_choice", "Industry is required.")
            return cleaned_data

        if not template_phases:
            self.add_error("template_phases", "Phases cannot be empty.")
            return cleaned_data

        if not template_name:
            self.add_error("template_name", "Template name cannot be empty.")

        if industry.templates.filter(template_name__iexact=template_name).exists():
            self.add_error(
                "template_name", "A template with that name already exists in the industry.")

        # Convert phases string to a list
        phases_list = [phase.strip()
                       for phase in template_phases.split(",") if phase.strip()]

        # Retrieve all templates in the selected industry
        industry_templates = industry.templates.prefetch_related("phases")

        for template in industry_templates:
            existing_phases = template.phases.values_list(
                "phase_name", flat=True)
            if set(phases_list) == set(existing_phases):
                raise ValidationError(
                    "Another template in the selected industry has the same phases."
                )

        return cleaned_data


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
