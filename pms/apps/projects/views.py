from typing import Any
from django.db import transaction
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectCreateForm, TemplateCreateForm
from . import models
from . import serializers


class IndustryListView(generics.ListAPIView):
    """
    A view that returns a list of all industries in the system. This view is used by the 
    frontend to populate the industry dropdown when creating a new template.

    Attributes:
        queryset (QuerySet): A queryset containing all industries in the system.
        serializer_class (Serializer): The serializer class used to serialize the industries.
    """
    queryset = models.Industry.objects.all()
    serializer_class = serializers.IndustrySerializser


class TemplateCreateView(LoginRequiredMixin, FormView):
    """
    Handles the creation of a new template in the database. This view processes
    the `TemplateCreateForm`, creates a `Template` instance along with associated 
    `TemplatePhase` instances if the form is valid.

    Attributes:
        form_class (Form): The form class used for creating a template.
        template_name (str): The template used for rendering the form.
        success_url (str): The URL to redirect to after a successful form submission.

    Methods:
        form_valid(form): Handles the form submission when the form is valid. Creates a new `Template` and 
                          `TemplatePhase` instances, then redirects to the success_url .
        get_success_url(): Returns the URL to redirect to after successfully creating a template, 
                           which defaults to the user's profile page.
    """
    form_class = TemplateCreateForm
    template_name = 'projects/template_create.html'
    success_url = reverse_lazy("home")

    @transaction.atomic
    def form_valid(self, form):
        industry = form.cleaned_data['industry_choice']
        template_name = form.cleaned_data['template_name']
        template_phases = form.cleaned_data['template_phases']

        template = models.Template.objects.create(
            industry=industry,
            template_name=template_name,
        )

        phases_list = [phase.strip()
                       for phase in template_phases.split(",") if phase.strip()]
        models.TemplatePhase.objects.bulk_create([
            models.TemplatePhase(template=template, phase_name=phase_name)
            for phase_name in phases_list
        ])

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('profile_page', kwargs={'username': self.request.user.username})


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = "projects/project_create.html"
    success_url = reverse_lazy('organization_detail', kwargs={
                               'organization_name_slug': ''})

    def get_form_kwargs(self):
        """Add custom keyword arguments for the form."""
        kwargs = super().get_form_kwargs()
        # Pass the 'organization_name_slug' from URL kwargs to the form
        kwargs['organization_name_slug'] = self.kwargs['organization_name_slug']
        return kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('organization_name_slug')
        print(context)
        print(f'slug {self.kwargs.get('organization_name_slug')}')
        return context

    @transaction.atomic
    def form_valid(self, form):
        template_id = form.cleaned_data.get('template')
        project_name = form.cleaned_data.get('project_name')
        project_name_slug = slugify(project_name)
        project = form.save(commit=False)
        project.project_name_slug = project_name_slug
        project.save()

        # add the creator as a member of the project.
        models.ProjectMember.objects.create(
            member=self.request.user, project=project)

        template = get_object_or_404(models.Template, pk=template_id)

        template_phases = template.phases.all()

        for template_phase in template_phases:
            models.ProjectPhase.objects.create(
                project=project, template_phase=template_phase)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('organization_detail', kwargs={'organization_name_slug': self.kwargs.get('organization_name_slug')})
